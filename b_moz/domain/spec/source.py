from b_moz.domain.base import DataFrameHolder

MODEL_KEY = "model"
SOURCE_KEY = "source"


class ModelSource(DataFrameHolder):
    columns = [MODEL_KEY, SOURCE_KEY]  # type: ignore

    def append_map(self, data: dict, links: list):
        model = data.get("model")
        if not model:
            raise ValueError("model is required")
        if links:
            for link in links:
                self.append([model, link])
