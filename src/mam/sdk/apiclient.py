import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class APIClient(object):
    environment_info = None  # MUST be set by caller

    def __init__(self, api_suffix, http_method_name, endpoint_suffix, path_arguments=None, query_arguments=None,
                 headers=None, body=None, files=None, *args, **kwargs):
        '''

        :param environment_info:
        :param api_suffix: suffix for api we're testing against (meta, master, etc.)
        :param http_method_name: http method to be used (in the form "GET", "POST", "DELETE", etc.)
        :param endpoint_suffix: endpoint path string, with path variables represented as {variable_name}
        :param path_arguments: dictionary of path argument values keyed by argument name (must match names in endpoint_suffix)
        :param query_arguments: dictionary of query argument values keyed by argument name. For values which are specified as arrays in the api, either lists or comma-delimited strings are accepted
        :param headers: header parameters to be passed in request (besides authentication header)
        :param body: json object to be supplied as the request body
        :param expected_response_code: number for expected response
        :param expected_response_body: expected response in json
        :param args:
        :param kwargs:

        NOTES:
        if orgId is specified in path_arguments, that value will be used. otherwise, the tenant specified in the
        json environment file will be used.
        /{orgId}/ should still be part of the endpoint suffix path though.
        only specify orgId in path_arguments if you're trying to test that the authentication specified in the json file
        doesn't work for other tenants.
        '''
        self.api_suffix = api_suffix
        self.http_method_name = http_method_name
        self.endpoint_suffix = endpoint_suffix
        self.path_arguments = path_arguments
        self.query_arguments = query_arguments
        self.headers = headers
        self.body = body
        self.files = files

    def call_api(self):

        if self.path_arguments is None:
            self.path_arguments = {}
        if self.headers is None:
            self.headers = {"Content-Type": 'application/json'}
        if self.query_arguments is None:
            self.query_arguments = {}
        if self.files is not None or self.headers == 'multipart':
            self.headers = None

        if "tenant_id" in self.environment_info and "orgId" not in self.path_arguments:
            self.path_arguments["orgId"] = self.environment_info["tenant_id"]

        # ignore None in query arguments; transform lists to comma-separated strings
        self.query_arguments = {key: (",".join(map(str, value)) if isinstance(value, list) else str(value)) for
                                key, value in self.query_arguments.items() if value is not None}

        format_dict = {}
        format_dict.update(APIClient.environment_info)
        format_dict["api_suffix"] = self.api_suffix
        url = "{base_url}/api/{api_suffix}/{version}".format(**format_dict)
        url = (url + self.endpoint_suffix).format(**self.path_arguments)
        print("url = " + url)

        cert_verify = self.environment_info["disableCertificateVerification"]

        if self.environment_info["isBasicAuth"]:  # Use basic authentication
            auth = (self.environment_info["API_USERNAME"], self.environment_info["API_PASSWORD"])
            response = requests.request(self.http_method_name, url, auth=auth, headers=self.headers,
                                        params=self.query_arguments, data=self.body, files=self.files,
                                        verify=cert_verify,
                                        timeout=60)

        else:  # Use token based authentication
            if self.headers is not None:
                headers = {**self.environment_info["authentication_header"], **self.headers}
            else:
                headers = {**self.environment_info["authentication_header"]}
            response = requests.request(self.http_method_name, url, headers=headers, params=self.query_arguments,
                                        data=self.body, files=self.files, verify=cert_verify, timeout=60)

        # Check the status code
        if response.status_code != 200:
            logger.debug(f'API call failed\n {response.text}')

        return response
