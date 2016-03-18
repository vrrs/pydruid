def build_dimension(dim):
    if isinstance(dim, DimensionSpec):
        dim = dim.build()

    return dim


class DimensionSpec(object):

    def __init__(self, dimension, output_name, extraction_function=None):
        self._dimension = dimension
        self._output_name = output_name
        self._extraction_function = extraction_function

    def build(self):
        dimension_spec = {
            'type': 'default',
            'dimension': self._dimension,
            'outputName': self._output_name
        }

        if self._extraction_function is not None:
            dimension_spec['type'] = 'extraction'
            dimension_spec['extractionFn'] = self._extraction_function.build()

        return dimension_spec


class ExtractionFunction(object):

    extraction_type = None

    def build(self):
        return {'type': self.extraction_type}


class BaseRegexExtraction(ExtractionFunction):

    def __init__(self, expr):
        super(BaseRegexExtraction, self).__init__()
        self._expr = expr

    def build(self):
        extractor = super(BaseRegexExtraction, self).build()
        extractor['expr'] = self._expr

        return extractor


class RegexExtraction(BaseRegexExtraction):

    extraction_type = 'regex'


class PartialExtraction(BaseRegexExtraction):

    extraction_type = 'partial'


class JavascriptExtraction(ExtractionFunction):

    extraction_type = 'javascript'

    def __init__(self, func, injective=False):
        super(JavascriptExtraction, self).__init__()
        self._func = func
        self._injective = injective

    def build(self):
        extractor = super(JavascriptExtraction, self).build()
        extractor['function'] = self._func
        extractor['injective'] = self._injective

        return extractor


class LookupExtraction(ExtractionFunction):

    extraction_type = 'lookup'
    lookup_type = None

    def __init__(self, retain_missing_values=False,
                 replace_missing_values=None, injective=False):
        super(LookupExtraction, self).__init__()
        self._retain_missing_values = retain_missing_values
        self._replace_missing_values = replace_missing_values
        self._injective = injective

    def build(self):
        extractor = super(LookupExtraction, self).build()
        extractor['lookup'] = self.build_lookup()
        extractor['retainMissingValue'] = self._retain_missing_values
        extractor['replaceMissingValueWith'] = self._replace_missing_values
        extractor['injective'] = self._injective

        return extractor

    def build_lookup(self):
        return {'type': self.lookup_type}


class MapLookupExtraction(LookupExtraction):

    lookup_type = 'map'

    def __init__(self, mapping, **kwargs):
        super(MapLookupExtraction, self).__init__(**kwargs)
        self._mapping = mapping

    def build_lookup(self):
        lookup = super(MapLookupExtraction, self).build_lookup()
        lookup['map'] = self._mapping

        return lookup