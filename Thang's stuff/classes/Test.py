# TODO: build test suite for pipelines


class Test:
    def make_test(self, filter_func):
        def test_condition(docs):
            return len(list(filter(filter_func, docs.values()))) == 0

        return test_condition

    def find_missing_location_field(self, doc):
        return "location" in doc.keys() and doc["location"] == ""

    def there_is_no_empty_location_field(self, docs):
        test = self.make_test(self.find_missing_location_field)
        test_result = test(docs)
        return test_result

    def is_longitude_negative(self, doc):
        return doc["longitude"] < 0

    def all_longitudes_are_negative(self, doc):
        test = self.make_test(self.is_longitude_negative)
        test_result = test(docs)
        return test_result
