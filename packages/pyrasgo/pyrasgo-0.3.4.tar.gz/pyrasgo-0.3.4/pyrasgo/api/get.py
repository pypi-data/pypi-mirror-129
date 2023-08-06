import pandas as pd
from typing import List, Optional, Dict

from .error import APIError
from pyrasgo import schemas as api
from pyrasgo.primitives import Collection, Feature, FeatureList, DataSource


class Get():

    def __init__(self):
        from .connection import Connection
        from pyrasgo.config import get_session_api_key
        from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()

    def collection(self, id: int) -> Collection:
        """
        Returns a Rasgo Collection (set of joined Features) matching the specified id
        """
        try:
            return Collection(api_object=self.api._get(f"/models/{id}", api_version=1).json())
        except:
            raise APIError(f"Collection {id} does not exist or this API key does not have access.")

    def collection_attributes(self, id: int) -> api.CollectionAttributes:
        """
        Returns a dict of attributes for a collection
        """
        try:
            response = self.api._get(f"/models/{id}/attributes", api_version=1).json()
            dict_out = {}
            for kv in response:
                dict_out[kv['key']] = kv['value']
            return api.CollectionAttributes(collectionId=id, attributes=dict_out)
        except:
            raise APIError(f"Collection {id} does not exist or this API key does not have access.")

    def collection_snapshot(self, model_id: int, index: int):
        return self.api._get(f"/models/{model_id}/snapshots/{index}", api_version=1).json()

    def collection_snapshots(self, model_id: int):
        return self.api._get(f"/models/{model_id}/snapshots", api_version=1).json()

    def collections(self, include_shared: bool=False) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) that I have author access to. Add an include_shared
        parameter to return all Rasgo Collections that I have any access to (author or shared access)
        :param include_shared: Boolean value indicating if the return should include all accessible collections
        """
        try:
            return [Collection(api_object=entry) for entry in self.api._get(f"/models", {"include_shared": include_shared}, api_version=1).json()]
        except:
            raise APIError("Collections do not exist or this API key does not have access.")

    def collections_by_attribute(self, key: str, value: str = None) -> List[Collection]:
        """
        Returns a list of Rasgo Collections that match an attribute
        """
        try:
            params = {"key": key}
            if value:
                params.update({"value": value})
            response = self.api._get(f"/models/attributes/models", params=params, api_version=1).json()
            return [Collection(api_object=r) for r in response]
        except:
            raise APIError(f"Key {key}: {value or 'Any'} does not exist or this API key does not have access.")

    def data_sources(self, with_features_only: bool = False) -> List[DataSource]:
        """
        Returns all DataSources available in your organization or Rasgo Community
        """
        try:
            response = self.api._get("/data-source", {"with_features_only": with_features_only}, api_version=1).json()
            return [DataSource(api_object=entry) for entry in response]
        except:
            raise APIError("Data Sources do not exist or this API key does not have access.")

    def data_source(self, id: int) -> DataSource:
        """
        Returns the DataSource with the specified id
        """
        try:
            response = self.api._get(f"/data-source/{id}", api_version=1).json()
            return DataSource(api_object=response)
        except:
            raise APIError(f"Data Source {id} does not exist or this API key does not have access.")

    def data_source_stats(self, id: int):
        """
        Returns the stats profile of the specificed data source
        """
        try:
            return self.api._get(f"/data-source/profile/{id}", api_version=1).json()
        except:
            raise APIError(f"Stats do not exist for DataSource {id}")

    def dataframes(self) -> List[api.Dataframe]:
        """
        Returns all Dataframes available in your organization or Rasgo Community
        """
        try:
            response = self.api._get("/dataframes", api_version=1).json()
            return [api.Dataframe(**entry) for entry in response]
        except:
            raise APIError("Dataframes do not exist or this API key does not have access.")

    def dataframe(self, unique_id: str) -> api.Dataframe:
        """
        Returns the Dataframe with the specified id
        """
        try:
            response = self.api._get(f"/dataframes/{unique_id}", api_version=1).json()
            return api.Dataframe(**response)
        except:
            raise APIError(f"Dataframe {unique_id} does not exist or this API key does not have access.")

    def feature(self, id: int) -> Feature:
        """
        Returns the Feature with the specified id
        """
        try:
            return Feature(api_object=self.api._get(f"/features/{id}", api_version=1).json())
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")

    def feature_attributes(self, id: int) -> api.FeatureAttributes:
        """
        Returns a dict of attributes for a feature
        """
        try:
            response = self.api._get(f"/features/{id}/attributes", api_version=1).json()
            dict_out = {}
            for kv in response:
                dict_out[kv['key']] = kv['value']
            return api.FeatureAttributes(featureId=id, attributes=dict_out)
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")

    def feature_attributes_log(self, id: int) -> tuple:
        """
        Returns a list of all attributes values logged to a feature over time
        """
        try:
            response = self.api._get(f"/features/{id}/attributes/log", api_version=1).json()
            lst_out = []
            for kv in response:
                dict_item={}
                dict_item[kv['key']] = kv.get('value', None)
                dict_item['updatedBy'] = kv.get('recordAuthorId', None)
                dict_item['updated'] = kv.get('recordTimestamp', None)
                lst_out.append(dict_item)
            return api.FeatureAttributesLog(featureId=id, attributes=lst_out)
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")


    def features_yml(self, data_source_id: int) -> api.FeaturesYML:
        """
        Returns the Features with the specified id
        """
        try:
            response = self.data_source(data_source_id)
            return api.FeaturesYML(
                name = response.name,
                sourceTable = response.dataTable.fqtn,
                dimensions = [{"columnName": d.columnName, "dataType": d.dataType, "granularity": d.granularity.name} for d in response.dimensions],
                features = response.features,
                sourceCode = response.sourceCode,
                sourceType = response.sourceType
            )
        except:
            raise APIError(f"Feature {id} does not exist or this API key does not have access.")

    def feature_stats(self, id: int) -> Optional[api.FeatureStats]:
        """
        Returns the stats profile for the specified Feature
        """
        try:
            stats_json = self.api._get(f"/features/{id}/stats", api_version=1).json()
            return api.FeatureStats(**stats_json["featureStats"])
        except:
            raise APIError(f"Stats do not exist yet for feature {id}.")

    def features(self) -> FeatureList:
        """
        Returns a list of Features available in your organization or Rasgo Community
        """
        try:
            return FeatureList(api_object=self.api._get("/features", api_version=1).json())
        except:
            raise APIError("Features do not exist or this API key does not have access.")

    def features_by_attribute(self, key: str, value: str = None) -> List[Feature]:
        """
        Returns a list of features that match an attribute
        """
        try:
            params = {"key": key}
            if value:
                params.update({"value": value})
            return FeatureList(api_object=self.api._get(f"/features/attributes/features", params=params, api_version=1).json())
        except:
            raise APIError(f"Key {key}: {value or 'Any'} does not exist or this API key does not have access.")

    def shared_collections(self) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) shared in my organization or in Rasgo community
        """
        try:
            return [Collection(api_object=entry) for entry in self.api._get(f"/models/shared", api_version=1).json()]
        except:
            raise APIError("Shared Collections do not exist or this API key does not have access.")

    def source_columns(self, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, data_type: Optional[str] = None) -> pd.DataFrame:
        """
        Returns a DataFrame of columns in Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_columns(table=table, database=database, schema=schema, data_type=data_type)

    def source_tables(self, database: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        Return a DataFrame of Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_tables(database=database, schema=schema)

    def transform(
        self,
        transform_id: int
    ) -> api.Transform:
        """Returns an individual transform
        """
        try:
            response = self.api._get(f"/transform/{transform_id}", api_version=1).json()
            return api.Transform(**response)
        except:
            raise APIError(f"Transform {transform_id} does not exist or this API key does not have access.")

    def transforms(self) -> List[api.Transform]:
        """Returns a list of available transforms
        """
        response = self.api._get(f"/transform", api_version=1).json()
        return [api.Transform(**r) for r in response]

    def user(self):
        return self.api._get("/users/me", api_version=1).json()
