from requests.exceptions import HTTPError
from typing import List, Optional, Union

from .error import APIError
from pyrasgo import schemas as api
from pyrasgo.primitives import Collection, Feature, FeatureList, DataSource
from pyrasgo.schemas.enums import Granularity, ModelType
from pyrasgo.schemas.feature import featureImportanceStats, ColumnProfiles


class Create():

    def __init__(self):
        from .connection import Connection
        from pyrasgo.config import get_session_api_key

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)

    def collection(self, name: str,
                   type: Union[str, ModelType],
                   granularity: Union[str, Granularity],
                   description: Optional[str] = None,
                   is_shared: Optional[bool] = False) -> Collection:
        try:
            # If not enum, convert to enum first.
            model_type = type.name
        except AttributeError:
            model_type = ModelType(type)

        try:
            # If not enum, convert to enum first.
            granularity = granularity.name
        except AttributeError:
            granularity = Granularity(granularity)

        content = {"name": name,
                   "type": model_type.value,
                   "granularities": [{"name": granularity.value}],
                   "isShared": is_shared
                   }
        if description:
            content["description"] = description
        response = self.api._post("/models", _json=content, api_version=1)
        return Collection(api_object=response.json())

    def data_source(self, table: str,
                    name: str,
                    source_type: str,
                    database: Optional[str] = None,
                    schema: Optional[str] = None,
                    source_code: Optional[str] = None,
                    domain: Optional[str] = None,
                    parent_source_id: Optional[int] = None) -> DataSource:
        data_source = api.DataSourceCreate(name=name,
                                           table=table,
                                           tableDatabase=database,
                                           tableSchema=schema,
                                           sourceCode=source_code,
                                           domain=domain,
                                           sourceType=source_type,
                                           parentId=parent_source_id)
        response = self.api._post("/data-source", data_source.dict(exclude_unset=True), api_version=1).json()
        return DataSource(api_object=response)

    def dataframe(self, unique_id: str,
                  name: str = None,
                  shared_status: str = 'organization',
                  column_hash: Optional[str] = None,
                  update_date: str = None) -> api.Dataframe:
        shared_status = 'organization' if shared_status not in ['public', 'private'] else shared_status
        dataframe = api.DataframeCreate(uniqueId=unique_id,
                                        name=name,
                                        sharedStatus=shared_status,
                                        columnHash=column_hash,
                                        updatedDate=update_date)
        try:
            response = self.api._post("/dataframes", dataframe.dict(exclude_unset=True), api_version=1).json()
        except HTTPError as e:
            error_message = f"Failed to create dataframe {unique_id}."
            if e.response.status_code == 409:
                error_message += f" This id is already in use in your organization. Dataframe IDs must be unique."
            raise APIError(error_message)
        return api.Dataframe(**response)

    def data_source_stats(self, data_source_id: int):
        """
        Sends an api request to build stats for a specified data source.
        """
        return self.api._post(f"/data-source/profile/{data_source_id}", api_version=1).json()

    def data_source_feature_stats(self, data_source_id: int):
        """
        Sends an api request to build stats for all features in a specified data source.
        """
        return self.api._post(f"/data-source/{data_source_id}/features/stats", api_version=1).json()

    def feature(self,
                data_source_id: int,
                display_name: str,
                column_name: str,
                description: str,
                #data_source_column_id: int,
                status: str,
                git_repo: str,
                tags: Optional[List[str]] = None) -> Feature:
        feature = api.FeatureCreate(name=display_name,
                                    code=column_name,
                                    description=description,
                                    dataSourceId=data_source_id,
                                    #dataSourceColumnId=data_source_column_id,
                                    orchestrationStatus=status,
                                    tags=tags or [],
                                    gitRepo=git_repo)
        try:
            response = self.api._post("/features/", feature.dict(exclude_unset=True), api_version=1).json()
        except HTTPError as e:
            error_message = f"Failed to create Feature {display_name}."
            if e.response.status_code == 409:
                error_message += f" {column_name} already has a feature associated with it. Try running update feature instead."
            raise APIError(error_message)
        return Feature(api_object=response)

    def feature_stats(self, feature_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self.api._post(f"/features/{feature_id}/stats", api_version=1).json()

    def feature_importance_stats(self, id: int, payload: featureImportanceStats):
        """
        Sends an api requrest to build feature importance stats for the specified model
        """
        return self.api._post(f"/models/{id}/stats/feature-importance", payload.dict(), api_version=1).json()

    def column_importance_stats(self, id: str, payload: featureImportanceStats):
        """
        Sends a json payload of importance from a dataFrame to the API so it can render in the WebApp
        """
        return self.api._post(f"/dataframes/{id}/feature-importance", payload.dict(), api_version=1).json()

    def dataframe_profile(self, id: str, payload: ColumnProfiles):
        """
        Send a json payload of a dataframe profile so it can render in the WebApp
        """
        return self.api._post(f"/dataframes/{id}/profile", payload.dict(), api_version=1).json()

    def transform(
        self,
        name: str,
        source_code: str,
        type: Optional[str] = None,
        arguments: Optional[List[dict]] = None
    ) -> api.Transform:
        """
        Create and return a new Transform in Rasgo
        Args:
            name: Name of the Transform
            source_code: Source code of transform
            type: Type of transform it is. Used for categorization only
            arguments: A list of arguments to supply to the transform
                       so it can render them in the UI. Each argument
                       must be a dict with the keys: 'name', 'description', and 'type'
                       values all strings for their corresponding value

        Returns:
            Created Transform obj
        """
        arguments = arguments if arguments else []

        transform = api.TransformCreate(
            name=name,
            type=type,
            sourceCode=source_code,
        )
        transform.arguments = [
            api.TransformArgumentCreate(**x) for x in arguments
        ]
        response = self.api._post("/transform", transform.dict(), api_version=1).json()
        return api.Transform(**response)
