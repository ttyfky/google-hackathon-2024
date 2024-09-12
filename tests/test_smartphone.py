from b_moz.domain.spec.smartphone import ModelStorage


class TestModelStorage:
    def test_format(self):
        assert ModelStorage.format("8GB") == "8GB"
        assert ModelStorage.format("1TB") == "1TB"
        assert ModelStorage.format("16 GB") == "16GB"
        assert ModelStorage.format("8 GB + 256 GB") == "256GB"
        assert ModelStorage.format("16GBフラッシュメモリ") == "16GB"
        assert ModelStorage.format("8 RAM + 256 GB memory") == "256GB"
        assert ModelStorage.format("18GB + 1TB") == "1TB"
        assert ModelStorage.format("12+256GB") == "256GB"

