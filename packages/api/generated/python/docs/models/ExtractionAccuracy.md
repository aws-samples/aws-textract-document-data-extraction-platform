# api_python_client.model.extraction_accuracy.ExtractionAccuracy

A collection of measures of the accuracy of data extracted for the form, computed once the form has been reviewed by a human

#### Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fieldDistancePercentage** | **int, float** | A percentage based on the Levenshtein Distance between the original extracted values and the human corrected values. Since it computes the minimum number of single-character edits (substitutions, insertions, deletions) required to transform the original to the reviewed, it acts as a measure much like &#x27;how much manual work was required for the review?&#x27; See https://en.wikipedia.org/wiki/Levenshtein_distance | 
**fieldCorrectnessPercentage** | **int, float** | The percentage of fields that were not changed during review | 
**any string name** | dict, frozendict, str, date, datetime, int, float, bool, Decimal, None, list, tuple, bytes | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

