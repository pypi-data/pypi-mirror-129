"""Module containing the classes to perform automatic OpenAPI contract validation."""
# TODO: support ${itemId} mapping instead of only "id"

import json as _json
import sys
from copy import deepcopy
from dataclasses import asdict, dataclass, field, make_dataclass
from enum import Enum
from itertools import zip_longest
from logging import getLogger
from pathlib import Path
from random import choice
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from uuid import uuid4

from openapi_core import create_spec
from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
    RequestsOpenAPIResponse,
)
from openapi_core.templating.paths.exceptions import ServerNotFound
from openapi_core.validation.response.validators import ResponseValidator
from requests import Response, Session
from requests.auth import AuthBase, HTTPBasicAuth
from robot.api import SkipExecution
from robot.libraries.BuiltIn import BuiltIn
from robotlibcore import keyword

from OpenApiDriver import value_utils
from OpenApiDriver.dto_base import (
    Dto,
    IdDependency,
    IdReference,
    PathPropertiesConstraint,
    PropertyValueConstraint,
    Relation,
    UniquePropertyValueConstraint,
)
from OpenApiDriver.dto_utils import DefaultDto, get_dto_class
from OpenApiDriver.value_utils import IGNORE

run_keyword = BuiltIn().run_keyword


logger = getLogger(__name__)


class ValidationLevel(str, Enum):
    """The available levels for the response_validation parameter."""

    DISABLED = "DISABLED"
    INFO = "INFO"
    WARN = "WARN"
    STRICT = "STRICT"


@dataclass
class RequestData:
    """Helper class to manage parameters used when making requests."""

    dto: Union[Dto, DefaultDto] = DefaultDto()
    dto_schema: Dict[str, Any] = field(default_factory=dict)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, Any] = field(default_factory=dict)


class OpenapiExecutors:  # pylint: disable=too-many-instance-attributes
    """Main class providing the keywords and core logic to perform endpoint validations."""

    def __init__(  # pylint: disable=too-many-arguments, too-many-locals
        self,
        openapi_specification: Dict[str, Any],
        origin: str = "",
        base_path: str = "",
        mappings_path: Union[str, Path] = "",
        username: str = "",
        password: str = "",
        security_token: str = "",
        auth: Optional[AuthBase] = None,
        response_validation: ValidationLevel = ValidationLevel.WARN,
        disable_server_validation: bool = True,
        require_body_for_invalid_url: bool = False,
        invalid_property_default_response: int = 422,
    ) -> None:
        self.openapi_spec: Dict[str, Any] = openapi_specification
        validation_spec = create_spec(self.openapi_spec)
        self.response_validator = ResponseValidator(
            spec=validation_spec,
            base_url=base_path,
        )
        self.session = Session()
        self.origin = origin
        self.base_url = f"{self.origin}{base_path}"
        # only username and password, security_token or auth object should be provided
        # if multiple are provided, username and password take precendence
        self.security_token = security_token
        self.auth = auth
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
        self.response_validation = response_validation
        self.disable_server_validation = disable_server_validation
        self.require_body_for_invalid_url = require_body_for_invalid_url
        self.invalid_property_default_response = invalid_property_default_response
        if mappings_path and str(mappings_path) != ".":
            mappings_path = Path(mappings_path)
            if not mappings_path.is_file():
                logger.warning(
                    f"mappings_path '{mappings_path}' is not a Python module."
                )
            # intermediate variable to ensure path.append is possible so we'll never
            # path.pop a location that we didn't append
            mappings_folder = str(mappings_path.parent)
            sys.path.append(mappings_folder)
            mappings_module_name = mappings_path.stem
            self.get_dto_class = get_dto_class(
                mappings_module_name=mappings_module_name
            )
            sys.path.pop()
        else:
            self.get_dto_class = get_dto_class(mappings_module_name="no_mapping")

    @keyword
    def test_unauthorized(self, endpoint: str, method: str) -> None:
        """
        Perform a request for `method` on the `endpoint`, with no authorization.

        This keyword only passes if the response code is 401: Unauthorized.

        Any authorization parameters used to initialize the library are
        ignored for this request.
        > Note: No headers or (json) body are send with the request. For security
        reasons, the authorization validation should be checked first.
        """
        url: str = run_keyword("get_valid_url", endpoint, method)
        response = self.session.request(
            method=method,
            url=url,
            verify=False,
        )
        assert response.status_code == 401

    @keyword
    def test_invalid_url(
        self, endpoint: str, method: str, expected_status_code: int = 404
    ) -> None:
        """
        Perform a request for the provided 'endpoint' and 'method' where the url for
        the `endpoint` is invalidated.

        This keyword will be `SKIPPED` if the endpoint contains no parts that
        can be invalidated.

        The optional `expected_status_code` parameter (default: 404) can be set to the
        expected status code for APIs that do not return a 404 on invalid urls.

        > Note: Depending on API design, the url may be validated before or after
        validation of headers, query parameters and / or (json) body. By default, no
        parameters are send with the request. The `require_body_for_invalid_url`
        parameter can be set to `True` if needed.
        """
        valid_url: str = run_keyword("get_valid_url", endpoint, method)

        if not (url := run_keyword("get_invalidated_url", valid_url)):
            raise SkipExecution(
                f"Endpoint {endpoint} does not contain resource references that "
                f"can be invalidated."
            )

        params, headers, json_data = None, None, None
        if self.require_body_for_invalid_url:
            request_data = self.get_request_data(method=method, endpoint=endpoint)
            params = request_data.params
            headers = request_data.headers
            dto = request_data.dto
            json_data = asdict(dto)
        response: Response = run_keyword(
            "authorized_request", url, method, params, headers, json_data
        )
        if response.status_code != expected_status_code:
            raise AssertionError(
                f"Response {response.status_code} was not {expected_status_code}"
            )

    @keyword
    def test_endpoint(self, endpoint: str, method: str, status_code: int) -> None:
        """
        Validate that performing the `method` operation on `endpoint` results in a
        `status_code` response.

        This is the main keyword to be used in the `Test Template` keyword when using
        the OpenApiDriver.

        The keyword calls other keywords to generate the neccesary data to perform
        the desired operation and validate the response against the openapi document.
        """
        json_data: Optional[Dict[str, Any]] = None
        original_data: Optional[Dict[str, Any]] = None

        url: str = run_keyword("get_valid_url", endpoint, method)
        request_data = self.get_request_data(method=method, endpoint=endpoint)
        params = request_data.params
        headers = request_data.headers
        dto = request_data.dto
        json_data = asdict(dto)
        # when patching, get the original data to check only patched data has changed
        if method == "PATCH":
            get_request_data = self.get_request_data(endpoint=endpoint, method="GET")
            get_params = get_request_data.params
            get_headers = get_request_data.headers
            response: Response = run_keyword(
                "authorized_request", url, "GET", get_params, get_headers
            )
            if response.ok:
                original_data = response.json()
        # in case of a status code indicating an error, ensure the error occurs
        if status_code >= 400:
            data_relations = dto.get_relations_for_error_code(status_code)
            parameter_relations = dto.get_parameter_relations_for_error_code(
                status_code
            )
            invalidation_keyword_data = {
                "get_invalid_json_data": [
                    "get_invalid_json_data",
                    data_relations,
                    request_data.dto_schema,
                    url,
                    method,
                    dto,
                    status_code,
                ],
                "invalidate_parameters": [
                    "invalidate_parameters",
                    params,
                    headers,
                    parameter_relations,
                    request_data.parameters,
                    status_code,
                ],
            }
            invalidation_keywords = []
            if data_relations:
                invalidation_keywords.append("get_invalid_json_data")
            if parameter_relations:
                invalidation_keywords.append("invalidate_parameters")
            if invalidation_keywords:
                if (
                    invalidation_keyword := choice(invalidation_keywords)
                ) == "get_invalid_json_data":
                    json_data = run_keyword(
                        *invalidation_keyword_data[invalidation_keyword]
                    )
                else:
                    params, headers = run_keyword(
                        *invalidation_keyword_data[invalidation_keyword]
                    )
            # if there are no relations to invalide and the status_code is the default
            # response_code for invalid properties, invalidate all properties
            elif status_code == self.invalid_property_default_response:
                json_data = run_keyword(
                    *invalidation_keyword_data["get_invalid_json_data"]
                )
                params, headers = run_keyword(
                    *invalidation_keyword_data["invalidate_parameters"]
                )
            else:
                logger.error(
                    f"No Dto mapping found to cause status_code {status_code}."
                )
        run_keyword(
            "perform_validated_request",
            endpoint,
            method,
            status_code,
            url,
            params,
            headers,
            json_data,
            original_data,
        )

    @keyword
    def perform_validated_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        url: str,
        params: Dict[str, Any],
        headers: Dict[str, str],
        json_data: Dict[str, Any],
        original_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        This keyword first calls the Authorized Request keyword, then the Validate
        Response keyword and finally validates is, for `DELETE` operations, whether
        the target resource was indeed deleted (OK response) or not (error responses).
        """
        response = run_keyword(
            "authorized_request", url, method, params, headers, json_data
        )
        if response.status_code != status_code:
            if not response.ok:
                if description := response.json().get("detail"):
                    pass
                else:
                    description = response.json().get("message")
                logger.error(f"{response.reason}: {description}")
            try:
                response_json = response.json()
            except Exception:
                response_json = {}
            logger.info(
                f"\nSend: {_json.dumps(json_data, indent=4, sort_keys=True)}"
                f"\nGot: {_json.dumps(response_json, indent=4, sort_keys=True)}"
            )
            raise AssertionError(
                f"Response status_code {response.status_code} was not {status_code}"
            )
        run_keyword("validate_response", endpoint, response, original_data)
        if method == "DELETE":
            get_request_data = self.get_request_data(endpoint=endpoint, method="GET")
            get_params = get_request_data.params
            get_headers = get_request_data.headers
            get_response = run_keyword(
                "authorized_request", url, "GET", get_params, get_headers
            )
            if response.ok:
                if get_response.ok:
                    raise AssertionError(
                        f"Resource still exists after deletion. Url was {url}"
                    )
                # if the endpoint supports GET, 404 is expected, if not 405 is expected
                if get_response.status_code not in [404, 405]:
                    logger.warning(
                        f"Unexpected response after deleting resource: Status_code "
                        f"{get_response.status_code} was received after trying to get {url} "
                        f"after sucessfully deleting it."
                    )
            else:
                if not get_response.ok:
                    raise AssertionError(
                        f"Resource could not be retrieved after failed deletion. "
                        f"Url was {url}, status_code was {get_response.status_code}"
                    )

    @keyword
    def get_valid_url(self, endpoint: str, method: str) -> str:
        """
        This keyword returns a valid url for the given `endpoint` and `method`.

        If the `endpoint` contains path parameters the Get Valid Id For Endpoint
        keyword will be executed to retrieve valid ids for the path parameters.

        > Note: if valid ids cannot be retrieved within the scope of the API, the
        `PathPropertiesConstraint` Relation can be used. More information can be found
        [here](https://marketsquare.github.io/robotframework-openapidriver/advanced_use.html).
        """
        dto_class = self.get_dto_class(endpoint=endpoint, method=method)
        relations = dto_class.get_relations()
        paths = [p.path for p in relations if isinstance(p, PathPropertiesConstraint)]
        if paths:
            url = f"{self.base_url}{choice(paths)}"
            return url
        endpoint_parts = list(endpoint.split("/"))
        for index, part in enumerate(endpoint_parts):
            if part.startswith("{") and part.endswith("}"):
                type_endpoint_parts = endpoint_parts[slice(index)]
                type_endpoint = "/".join(type_endpoint_parts)
                existing_id: str = run_keyword(
                    "get_valid_id_for_endpoint", type_endpoint, method
                )
                if not existing_id:
                    raise Exception
                endpoint_parts[index] = existing_id
        resolved_endpoint = "/".join(endpoint_parts)
        url = f"{self.base_url}{resolved_endpoint}"
        return url

    @keyword
    def get_valid_id_for_endpoint(self, endpoint: str, method: str) -> str:
        """
        Support keyword that returns the `id` for an existing resource at `endpoint`.

        To prevent resource conflicts with other test cases, a new resource is created
        (POST) if possible.
        """
        url: str = run_keyword("get_valid_url", endpoint, method)
        # Try to create a new resource to prevent conflicts caused by
        # operations performed on the same resource by other test cases
        request_data = self.get_request_data(endpoint=endpoint, method="POST")
        params = request_data.params
        headers = request_data.headers
        dto = request_data.dto
        try:
            json_data = asdict(dto)
            response: Response = run_keyword(
                "authorized_request", url, "POST", params, headers, json_data
            )
        except NotImplementedError as exception:
            logger.debug(f"get_valid_id_for_endpoint POST failed: {exception}")
            # For endpoints that do no support POST, try to get an existing id using GET
            try:
                request_data = self.get_request_data(endpoint=endpoint, method="GET")
                params = request_data.params
                headers = request_data.headers
                response = run_keyword(
                    "authorized_request", url, "GET", params, headers
                )
                assert response.ok
                response_data: Union[
                    Dict[str, Any], List[Dict[str, Any]]
                ] = response.json()
                if isinstance(response_data, list):
                    valid_ids: List[str] = [item["id"] for item in response_data]
                    logger.debug(
                        f"get_valid_id_for_endpoint: returning choice from list {valid_ids}"
                    )
                    return choice(valid_ids)
                if valid_id := response_data.get("id"):
                    logger.debug(f"get_valid_id_for_endpoint: returning {valid_id}")
                    return valid_id
                valid_ids = [item["id"] for item in response_data["items"]]
                logger.debug(
                    f"get_valid_id_for_endpoint: returning choice from items {valid_ids}"
                )
                return choice(valid_ids)
            except Exception as exception:
                logger.debug(
                    f"Failed to get a valid id using GET on {url}"
                    f"\nException was {exception}"
                )
                raise exception

        assert (
            response.ok
        ), f"get_valid_id_for_endpoint received status_code {response.status_code}"
        response_data = response.json()
        if prepared_body := response.request.body:
            if isinstance(prepared_body, bytes):
                send_json = _json.loads(prepared_body.decode("UTF-8"))
            else:
                send_json = _json.loads(prepared_body)
        else:
            send_json = None
        # no support for retrieving an id from an array returned on a POST request
        if isinstance(response_data, list):
            raise NotImplementedError(
                f"Unexpected response body for POST request: expected an object but "
                f"received an array ({response_data})"
            )
        # POST on /resource_type/{id}/array_item/ will return the updated {id} resource
        # instead of a newly created resource. In this case, the send_json must be
        # in the array of the 'array_item' property on {id}
        send_path: str = response.request.path_url
        response_path: Optional[str] = response_data.get("href", None)
        if response_path and (send_path not in response_path) and send_json:
            property_to_check = send_path.replace(response_path, "")[1:]
            item_list: List[Dict[str, Any]] = response_data[property_to_check]
            # Use the (mandatory) id to get the POSTed resource from the list
            [valid_id] = [
                item["id"] for item in item_list if item["id"] == send_json["id"]
            ]
        else:
            valid_id = response_data["id"]
        return valid_id

    def get_request_data(self, endpoint: str, method: str) -> RequestData:
        """Return an object with valid request data for body, headers and query params."""
        method = method.lower()
        # The endpoint can contain already resolved Ids that have to be matched
        # against the parametrized endpoints in the paths section.
        spec_endpoint = self.get_parametrized_endpoint(endpoint)
        try:
            method_spec = self.openapi_spec["paths"][spec_endpoint][method]
        except KeyError as exception:
            raise NotImplementedError(
                f"method '{method}' not suported on '{spec_endpoint}"
            ) from exception
        dto_class = self.get_dto_class(endpoint=spec_endpoint, method=method)

        parameters = method_spec.get("parameters", [])
        parameter_relations = dto_class.get_parameter_relations()
        query_params = [p for p in parameters if p.get("in") == "query"]
        header_params = [p for p in parameters if p.get("in") == "header"]
        params = self.get_parameter_data(query_params, parameter_relations)
        headers = self.get_parameter_data(header_params, parameter_relations)

        if (body_spec := method_spec.get("requestBody", None)) is None:
            if dto_class == DefaultDto:
                dto_instance: Dto = DefaultDto()
            else:
                dto_class = make_dataclass(
                    cls_name=method_spec["operationId"],
                    fields=[],
                    bases=(dto_class,),
                )
                dto_instance = dto_class()
            return RequestData(
                dto=dto_instance,
                parameters=parameters,
                params=params,
                headers=headers,
            )
        # Content should be a single key/value entry, so use tuple assignment
        (content_type,) = body_spec["content"].keys()
        if content_type != "application/json":
            # At present no supported for other types.
            raise NotImplementedError(f"content_type '{content_type}' not supported")
        content_schema = body_spec["content"][content_type]["schema"]
        # TODO: is resolve_schema still needed?
        resolved_schema: Dict[str, Any] = self._resolve_schema(content_schema)
        dto_data = self.get_json_data_for_dto_class(
            schema=resolved_schema,
            dto_class=dto_class,
            operation_id=method_spec.get("operationId"),
        )
        if dto_data is None:
            dto_instance = DefaultDto()
        else:
            fields: List[Tuple[str, type]] = []
            for key, value in dto_data.items():
                fields.append((key, type(value)))
            dto_class = make_dataclass(
                cls_name=method_spec["operationId"],
                fields=fields,
                bases=(dto_class,),
            )
            dto_instance = dto_class(**dto_data)  # type: ignore[call-arg]
        return RequestData(
            dto=dto_instance,
            dto_schema=resolved_schema,
            parameters=parameters,
            params=params,
            headers=headers,
        )

    def get_parametrized_endpoint(self, endpoint: str) -> str:
        """
        Get the parametrized endpoint as found in the `paths` section of the openapi
        document from a (partially) resolved endpoint.
        """

        def match_parts(parts: List[str], spec_parts: List[str]) -> bool:
            for part, spec_part in zip_longest(parts, spec_parts, fillvalue="Filler"):
                if part == "Filler" or spec_part == "Filler":
                    return False
                if part != spec_part and not spec_part.startswith("{"):
                    return False
            return True

        endpoint_parts = endpoint.split("/")
        # trailing '/' should not be matched
        if len(endpoint_parts) > 2 and endpoint_parts[-1] == "":
            endpoint_parts.pop(-1)
        spec_endpoints: List[str] = {**self.openapi_spec}["paths"].keys()
        for spec_endpoint in spec_endpoints:
            spec_endpoint_parts = spec_endpoint.split("/")
            if match_parts(endpoint_parts, spec_endpoint_parts):
                return spec_endpoint
        raise ValueError(f"{endpoint} not matched to openapi_spec path")

    @staticmethod
    def get_parameter_data(
        parameters: List[Dict[str, Any]],
        parameter_relations: List[Relation],
    ) -> Dict[str, str]:
        """Generate a valid list of key-value pairs for all parameters."""
        result: Dict[str, str] = {}
        value: Any = None
        for parameter in parameters:
            parameter_name = parameter["name"]
            parameter_schema = parameter["schema"]
            relations = [
                r for r in parameter_relations if r.property_name == parameter_name
            ]
            if constrained_values := [
                r.values for r in relations if isinstance(r, PropertyValueConstraint)
            ]:
                value = choice(*constrained_values)
                if value is IGNORE:
                    continue
                result[parameter_name] = str(value)
                continue
            value = value_utils.get_valid_value(parameter_schema)
            # By the http standard, query string and header values must be strings
            result[parameter_name] = str(value)
        return result

    @keyword
    def get_json_data_for_dto_class(
        self, schema: Dict[str, Any], dto_class: Type[Dto], operation_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a valid (json-compatible) dict for all the `dto_class` properties.
        """

        def get_constrained_values(property_name: str) -> List[Any]:
            relations = dto_class.get_relations()
            values_list = [
                c.values
                for c in relations
                if (
                    isinstance(c, PropertyValueConstraint)
                    and c.property_name == property_name
                )
            ]
            # values should be empty or contain 1 list of allowed values
            return values_list.pop() if values_list else []

        def get_dependent_id(property_name: str, operation_id: str) -> Optional[str]:
            relations = dto_class.get_relations()
            # multiple get paths are possible based on the operation being performed
            id_get_paths = [
                (d.get_path, d.operation_id)
                for d in relations
                if (isinstance(d, IdDependency) and d.property_name == property_name)
            ]
            if not id_get_paths:
                return None
            if len(id_get_paths) == 1:
                id_get_path, _ = id_get_paths.pop()
            else:
                try:
                    [id_get_path] = [
                        path
                        for path, operation in id_get_paths
                        if operation == operation_id
                    ]
                # There could be multiple get_paths, but not one for the current operation
                except ValueError:
                    return None
            valid_id = self.get_valid_id_for_endpoint(
                endpoint=id_get_path, method="GET"
            )
            logger.debug(f"get_dependent_id for {id_get_path} returned {valid_id}")
            return valid_id

        json_data: Dict[str, Any] = {}

        for property_name in schema.get("properties", []):
            value_schema = schema["properties"][property_name]
            property_type = value_schema["type"]
            if constrained_values := get_constrained_values(property_name):
                # do not add properties that are configured to be ignored
                if IGNORE in constrained_values:
                    continue
                json_data[property_name] = choice(constrained_values)
                continue
            if dependent_id := get_dependent_id(
                property_name=property_name, operation_id=operation_id
            ):
                json_data[property_name] = dependent_id
                continue
            if property_type == "object":
                default_dto = self.get_dto_class(endpoint="", method="")
                object_data = self.get_json_data_for_dto_class(
                    schema=value_schema,
                    dto_class=default_dto,
                    operation_id="",
                )
                json_data[property_name] = object_data
                continue
            json_data[property_name] = value_utils.get_valid_value(value_schema)
        return json_data

    @keyword
    def get_invalidated_url(self, valid_url: str) -> Optional[str]:
        """
        Return an url with all the path parameters in the `valid_url` replaced by a
        random UUID. If the `valid_url` does not contain any parameters, None is returned.
        """
        endpoint = valid_url.replace(self.base_url, "")
        endpoint_parts = endpoint.split("/")
        # first part will be '' since an endpoint starts with /
        endpoint_parts.pop(0)
        parameterized_endpoint = self.get_parametrized_endpoint(endpoint=endpoint)
        parameterized_url = self.base_url + parameterized_endpoint
        valid_url_parts = list(reversed(valid_url.split("/")))
        parameterized_parts = reversed(parameterized_url.split("/"))
        for index, (parameterized_part, _) in enumerate(
            zip(parameterized_parts, valid_url_parts)
        ):
            if parameterized_part.startswith("{") and parameterized_part.endswith("}"):
                valid_url_parts[index] = uuid4().hex
                valid_url_parts.reverse()
                invalid_url = "/".join(valid_url_parts)
                return invalid_url
        # TODO: add support for header / query parameters that can be invalidated
        return None

    @keyword
    def get_invalid_json_data(
        self,
        data_relations: List[Relation],
        schema: Dict[str, Any],
        url: str,
        method: str,
        dto: Dto,
        status_code: int,
    ) -> Dict[str, Any]:
        """
        Return `json_data` based on the `dto` that will cause the provided `status_code`
        for the `method` operation on the `url`.

        > Note: applicable UniqueProperyValueConstraint and IdReference Relations are
            considered before changes to `json_data` are made.
        """
        if not data_relations:
            if not schema:
                raise AssertionError(
                    "Failed to invalidate: no data_relations and missing schema."
                )
            json_data = dto.get_invalidated_data(
                schema=schema,
                status_code=status_code,
                invalid_property_default_code=self.invalid_property_default_response,
            )
            return json_data
        resource_relation = choice(data_relations)
        if isinstance(resource_relation, UniquePropertyValueConstraint):
            json_data = run_keyword(
                "get_json_data_with_conflict", url, method, dto, status_code
            )
        elif isinstance(resource_relation, IdReference):
            run_keyword("ensure_in_use", url, resource_relation)
            json_data = asdict(dto)
        else:
            json_data = dto.get_invalidated_data(
                schema=schema,
                status_code=status_code,
                invalid_property_default_code=self.invalid_property_default_response,
            )
        return json_data

    @keyword
    def invalidate_parameters(
        self,
        params: Dict[str, Any],
        headers: Dict[str, str],
        relations: List[Relation],
        parameters: List[Dict[str, Any]],
        status_code: int,
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Returns a version of `params, headers` that has been modified to cause the
        provided `status_code`.
        """
        if not params and not headers:
            return params, headers
        if any([params, headers]) and not parameters:
            logger.warning(
                "Could not invalidate parameters: parameters list was empty."
            )
            return params, headers
        # ensure we're not modifying mutable arguments
        params = deepcopy(params)
        headers = deepcopy(headers)
        relations_for_status_code = [
            r
            for r in relations
            if isinstance(r, PropertyValueConstraint) and r.error_code == status_code
        ]
        if status_code == self.invalid_property_default_response:
            parameter_data = choice(parameters)
            parameter_to_invalidate = parameter_data["name"]
        else:
            parameter_names = [r.property_name for r in relations_for_status_code]
            parameter_to_invalidate = choice(parameter_names)
            [parameter_data] = [
                d for d in parameters if d["name"] == parameter_to_invalidate
            ]
        relations_for_parameter = [
            r.values
            for r in relations_for_status_code
            if r.property_name == parameter_to_invalidate
        ]
        values_from_constraint = (
            relations_for_parameter[0] if relations_for_parameter else None
        )
        if parameter_to_invalidate in params.keys():
            valid_value = params[parameter_to_invalidate]
        elif parameter_to_invalidate in headers.keys():
            valid_value = headers[parameter_to_invalidate]
        else:
            valid_value = value_utils.get_valid_value(parameter_data["schema"])
        invalid_value = value_utils.get_invalid_value(
            value_schema=parameter_data["schema"],
            current_value=valid_value,
            values_from_constraint=values_from_constraint,
        )

        if parameter_to_invalidate in params.keys():
            params[parameter_to_invalidate] = invalid_value
        else:
            headers[parameter_to_invalidate] = str(invalid_value)
        return params, headers

    @keyword
    def ensure_in_use(self, url: str, resource_relation: IdReference) -> None:
        """
        Ensure that the `id` of the resource referenced by the `url` is used by the
        resource defined by the `resource_relation`.
        """
        endpoint = url.replace(self.base_url, "")
        endpoint_parts = endpoint.split("/")
        # first part will be '' since an endpoint starts with /
        endpoint_parts.pop(0)
        parameterized_endpoint = self.get_parametrized_endpoint(endpoint=endpoint)
        if parameterized_endpoint.endswith("}"):
            resource_id = endpoint_parts[-1]
        else:
            resource_id = ""
        post_endpoint = resource_relation.post_path
        property_name = resource_relation.property_name
        request_data = self.get_request_data(method="POST", endpoint=post_endpoint)
        params = request_data.params
        headers = request_data.headers
        dto = request_data.dto
        json_data = asdict(dto)
        if resource_id:
            json_data[property_name] = resource_id
        post_url: str = run_keyword("get_valid_url", post_endpoint, "POST")
        response: Response = run_keyword(
            "authorized_request", post_url, "POST", params, headers, json_data
        )
        if not response.ok:
            logger.debug(
                f"POST on {post_url} with json {json_data} failed: {response.json()}"
            )
            response.raise_for_status()

    @keyword
    def get_json_data_with_conflict(
        self, url: str, method: str, dto: Dto, conflict_status_code: int
    ) -> Dict[str, Any]:
        """
        Return `json_data` based on the `UniqueProperyValueConstraint` that must be
        returned by the `get_relations` implementation on the `dto` for the given
        `conflict_status_code`.
        """
        json_data = asdict(dto)
        unique_property_value_constraints = [
            r
            for r in dto.get_relations()
            if isinstance(r, UniquePropertyValueConstraint)
        ]
        for relation in unique_property_value_constraints:
            json_data[relation.property_name] = relation.value
            # create a new resource that the original request will conflict with
            if method in ["PATCH", "PUT"]:
                post_url_parts = url.split("/")[:-1]
                post_url = "/".join(post_url_parts)
                # the PATCH or PUT may use a different dto than required for POST
                # so a valid POST dto must be constructed
                endpoint = post_url.replace(self.base_url, "")
                request_data = self.get_request_data(endpoint=endpoint, method="POST")
                post_json = asdict(request_data.dto)
                for key in post_json.keys():
                    if key in json_data:
                        post_json[key] = json_data.get(key)
            else:
                post_url = url
                post_json = json_data
            endpoint = post_url.replace(self.base_url, "")
            request_data = self.get_request_data(endpoint=endpoint, method="POST")
            params = request_data.params
            headers = request_data.headers
            response: Response = run_keyword(
                "authorized_request", post_url, "POST", params, headers, post_json
            )
            # conflicting resource may already exist
            assert (
                response.ok or response.status_code == conflict_status_code
            ), f"get_json_data_with_conflict received {response.status_code}: {response.json()}"
            return json_data
        raise ValueError(
            f"No UniquePropertyValueConstraint in the get_relations list on dto {dto}."
        )

    def _resolve_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        # schema is mutable, so copy to prevent mutation of original schema argument
        resolved_schema: Dict[str, Any] = schema.copy()
        if schema_parts := resolved_schema.pop("allOf", None):
            for schema_part in schema_parts:
                resolved_part = self._resolve_schema(schema_part)
                resolved_schema = self._merge_schemas(resolved_schema, resolved_part)
        return resolved_schema

    @staticmethod
    def _merge_schemas(first: Dict[str, Any], second: Dict[str, Any]) -> Dict[str, Any]:
        merged_schema = first.copy()
        for key, value in second.items():
            # for exisiting keys, merge dict and list values, leave others unchanged
            if key in merged_schema.keys():
                if isinstance(value, dict):
                    # if the key holds a dict, merge the values (e.g. 'properties')
                    merged_schema[key].update(value)
                elif isinstance(value, list):
                    # if the key holds a list, extend the values (e.g. 'required')
                    merged_schema[key].extend(value)
                else:
                    logger.debug(
                        f"key '{key}' with value '{merged_schema[key]}' not "
                        f"updated to '{value}'"
                    )
            else:
                merged_schema[key] = value
        return merged_schema

    @keyword
    def validate_response(
        self,
        endpoint: str,
        response: Response,
        original_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Validate the `response` by performing the following validations:
        - validate the `response` against the openapi schema for the `endpoint`
        - validate that the response does not contain extra properties
        - validate that a href, if present, refers to the correct resource
        - validate that the value for a property that is in the response is equal to
            the property value that was send
        - validate that no `original_data` is preserved when performing a PUT operation
        - validate that a PATCH operation only updates the provided properties
        """
        if response.status_code == 204:
            assert not response.content
            return None
        # validate the response against the schema
        openapi_request = RequestsOpenAPIRequest(response.request)
        openapi_response = RequestsOpenAPIResponse(response)
        validation_result = self.response_validator.validate(
            request=openapi_request,
            response=openapi_response,
        )
        if self.disable_server_validation:
            validation_result.errors = [
                e for e in validation_result.errors if not isinstance(e, ServerNotFound)
            ]
        if self.response_validation == ValidationLevel.STRICT:
            validation_result.raise_for_errors()
        if self.response_validation in [ValidationLevel.WARN, ValidationLevel.INFO]:
            for validation_error in validation_result.errors:
                if self.response_validation == ValidationLevel.WARN:
                    logger.warning(validation_error)
                else:
                    logger.info(validation_error)

        request_method = response.request.method
        if request_method is None:
            logger.warning(
                f"Could not validate response for endpoint {endpoint}; no method found "
                f"on the request property of the provided response."
            )
            return None
        response_spec = self._get_response_spec(
            endpoint=endpoint,
            method=request_method,
            status_code=response.status_code,
        )
        # content should be a single key/value entry, so use tuple assignment
        (content_type,) = response_spec["content"].keys()
        if content_type != "application/json":
            # at present, only json reponses are supported
            raise NotImplementedError(f"content_type '{content_type}' not supported")
        if response.headers["Content-Type"] != content_type:
            raise ValueError(
                f"Content-Type '{response.headers['Content-Type']}' of the response "
                f"is not '{content_type}' as specified in the OpenAPI document."
            )
        json_response = response.json()

        response_schema = response_spec["content"][content_type]["schema"]
        resolved_schema = self._resolve_schema(response_schema)
        if list_item_schema := resolved_schema.get("items"):
            if not isinstance(json_response, list):
                raise AssertionError(
                    f"Response schema violation: the schema specifies an array as "
                    f"response type but the response was of type {type(json_response)}."
                )
            # at present, only lists of resource objects are supported
            if list_item_schema.get("type") != "object":
                raise NotImplementedError(
                    f"response validation of lists of "
                    f"{list_item_schema.get('type')} not supported"
                )
            expected_properties = list_item_schema["properties"]
            for resource in json_response:
                run_keyword(
                    "validate_resource_properties", resource, expected_properties
                )
            # no further validation; value validation of individual resources should
            # be performed on the endpoints for the specific resource
            return None

        run_keyword(
            "validate_resource_properties", json_response, resolved_schema["properties"]
        )
        # ensure the href is valid if present in the response
        if href := json_response.get("href"):
            url = f"{self.origin}{href}"
            endpoint = url.replace(self.base_url, "")
            request_data = self.get_request_data(endpoint=endpoint, method="GET")
            params = request_data.params
            headers = request_data.headers
            get_response = self.authorized_request(
                url=url, method="GET", params=params, headers=headers
            )
            assert (
                get_response.json() == json_response
            ), f"{get_response.json()} not equal to original {json_response}"
        # every property that was sucessfully send and that is in the response
        # schema must have the value that was send
        if response.ok and response.request.method in ["POST", "PUT", "PATCH"]:
            run_keyword("validate_send_response", response, original_data)
        return None

    @staticmethod
    @keyword
    def validate_resource_properties(
        resource: Dict[str, Any], schema_properties: Dict[str, Any]
    ) -> None:
        """
        Validate that the 'resource' does not contain any properties that are not
        defined in the `schema_properties`.
        """
        if resource.keys() != schema_properties.keys():
            expected_property_names = sorted(schema_properties.keys())
            property_names_in_resource = sorted(resource.keys())
            raise AssertionError(
                f"Response schema violation: the response contains properties that are "
                f"not specified in the schema."
                f"\n\tExpected: {expected_property_names}"
                f"\n\tGot: {property_names_in_resource}"
            )

    @staticmethod
    @keyword
    def validate_send_response(
        response: Response, original_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Validate that each property that was send that is in the response has the value
        that was send.
        In case a PATCH request, validate that only the properties that were patched
        have changed and that other properties are still at their pre-patch values.
        """
        reference = response.json()
        if prepared_body := response.request.body:
            if isinstance(prepared_body, bytes):
                send_json = _json.loads(prepared_body.decode("UTF-8"))
            else:
                send_json = _json.loads(prepared_body)
        else:
            logger.warning(
                "Could not validate send response; the body of the request property "
                "on the provided response was None."
            )
            return None
        # POST on /resource_type/{id}/array_item/ will return the updated {id} resource
        # instead of a newly created resource. In this case, the send_json must be
        # in the array of the 'array_item' property on {id}
        send_path: str = response.request.path_url
        response_path = reference.get("href", None)
        if response_path and send_path not in response_path:
            property_to_check = send_path.replace(response_path, "")[1:]
            if reference.get(property_to_check) and isinstance(
                reference[property_to_check], list
            ):
                item_list: List[Dict[str, Any]] = reference[property_to_check]
                # Use the (mandatory) id to get the POSTed resource from the list
                [reference] = [
                    item for item in item_list if item["id"] == send_json["id"]
                ]
        for key, value in send_json.items():
            # sometimes, a property in the request is not in the response, e.g. a password
            if key not in reference.keys():
                continue
            if value is not None:
                # if a None value is send, the target property should be cleared or
                # reverted to the default value (which cannot be specified in the
                # openapi document)
                assert reference[key] == value, (
                    f"Received value for {key} '{reference[key]}' does not "
                    f"match '{value}' in the {response.request.method} request"
                    f"\nSend: {_json.dumps(send_json, indent=4, sort_keys=True)}"
                    f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                )
        # In case of PATCH requests, ensure that only send properties have changed
        if original_data:
            for key, value in original_data.items():
                if key not in send_json.keys():
                    assert value == reference[key], (
                        f"Received value for {key} '{reference[key]}' does not "
                        f"match '{value}' in the pre-patch data"
                        f"\nPre-patch: {_json.dumps(original_data, indent=4, sort_keys=True)}"
                        f"\nGot: {_json.dumps(reference, indent=4, sort_keys=True)}"
                    )
        return None

    def _get_response_spec(
        self, endpoint: str, method: str, status_code: int
    ) -> Dict[str, Any]:
        method = method.lower()
        status = str(status_code)
        spec = {**self.openapi_spec}["paths"][endpoint][method]["responses"][status]
        return spec

    @keyword
    def authorized_request(
        self,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Response:
        """
        Perform a request using the security token or authentication set in the library.

        > Note: provided username / password or auth objects take precedence over token
            based security
        """
        # if both an auth object and a token are available, auth takes precedence
        if self.security_token and not self.auth:
            security_header = {"Authorization": self.security_token}
            headers = headers if headers else {}
            headers.update(security_header)
        response = self.session.request(
            url=url,
            method=method,
            params=params,
            headers=headers,
            json=json,
            auth=self.auth,
            verify=False,
        )
        logger.debug(f"Response text: {response.text}")
        return response
