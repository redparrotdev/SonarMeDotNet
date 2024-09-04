
class AppConfig:

    KEY_APP_KEY = "app_key"
    KEY_APP_TOKEN = "app_token"
    KEY_DOCKERFILE_NAME = "dockerfile_name"
    KEY_DEFAULT_IMAGE = "default_image"
    KEY_WORKDIR = "workdir"
    KEY_SONAR_HOST = "sonar_host"
    KEY_SONAR_PORT = "sonar_port"
    KEY_DELETE_DOCKERFILE = "delete_dockerfile"
    KEY_DELETE_IMAGE = "delete_image"
    KEY_COVERAGE_FILE_NAME = "coverage_file_name"
    KEY_TOOLS_ENV_PATH = "tools_env_path"
    KEY_EXCLUDE = "exclude"

    DEFAULT_DOCKERFILE_NAME = "sonarme.dockerfile"
    DEFAULT_IMAGE = "mcr.microsoft.com/dotnet/sdk:8.0"
    DEFAULT_WORKDIR = "/code"
    DEFAULT_TOOLS_ENV_PATH = "$PATH:/root/.dotnet/tools"
    DEFAULT_SONAR_HOST = "http://localhost"
    DEFAULT_SONAR_PORT = 9000
    DEFAULT_COVERAGE_FILE_NAME = "coverage.xml"
    DEFAULT_DELETE_DOCKERFILE = True
    DEFAULT_DELETE_IMAGE = True

    def __init__(self, configs: dict):
        
        self.__json_data = configs

        self.__dockerfile_name = self.__json_data.setdefault(AppConfig.KEY_DOCKERFILE_NAME, AppConfig.DEFAULT_DOCKERFILE_NAME)
        self.__image = self.__json_data.setdefault(AppConfig.KEY_DEFAULT_IMAGE, AppConfig.DEFAULT_IMAGE)
        self.__workdir = self.__json_data.setdefault(AppConfig.KEY_WORKDIR, AppConfig.DEFAULT_WORKDIR)
        self.__tools_env_path = self.__json_data.setdefault(AppConfig.KEY_TOOLS_ENV_PATH, AppConfig.DEFAULT_TOOLS_ENV_PATH)
        self.__sonar_host = self.__json_data.setdefault(AppConfig.KEY_SONAR_HOST, AppConfig.DEFAULT_SONAR_HOST)
        self.__sonar_port = self.__json_data.setdefault(AppConfig.KEY_SONAR_PORT, AppConfig.DEFAULT_SONAR_PORT)
        self.__coverage_file_name = self.__json_data.setdefault(AppConfig.KEY_COVERAGE_FILE_NAME, AppConfig.DEFAULT_COVERAGE_FILE_NAME)
        self.__delete_dockerfile = self.__json_data.setdefault(AppConfig.KEY_DELETE_DOCKERFILE, AppConfig.DEFAULT_DELETE_DOCKERFILE)
        self.__delete_image = self.__json_data.setdefault(AppConfig.KEY_DELETE_IMAGE, AppConfig.DEFAULT_DELETE_IMAGE)
        self.__exclude = self.__json_data.setdefault(AppConfig.KEY_EXCLUDE, list())

    @property
    def data(self) -> dict: return self.__json_data.copy()
    
    @property
    def dockerfile_name(self): return self.__dockerfile_name

    @property
    def image(self): return self.__image

    @property
    def workdir(self): return self.__workdir

    @property
    def tools_env_path(self): return self.__tools_env_path

    @property
    def sonar_host(self): return self.__sonar_host

    @property
    def sonar_port(self): return self.__sonar_port

    @property
    def coverage_file_name(self): return self.__coverage_file_name

    @property
    def delete_dockerfile(self): return self.__delete_dockerfile

    @property
    def delete_image(self): return self.__delete_image

    @property
    def exclude(self): return self.__exclude
