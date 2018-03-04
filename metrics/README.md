# Metrics
Collection of scripts and data to compute various evaluation metrics for sanskrit_parser library.

## word_accuracy_metrics.py
Test accuracy of different word-level lookup schemes.
Uses annotated data from the Digital Corpus of Sanskrit
database to evaluate how many words are recognized by 
each of the lexical lookup schemes. Also checks if the
annotated root of the word in the DCS matches the stems
returned by the lexical lookup schemes.

Saves a log of which words are not correctly recognized for
further analysis.

Current output should look similar to:
```
--------------------------------------------------
Metrics for inria
--------------------------------------------------
Recognized 1438669 / 1932518 words, accuracy = 74.45%
Correct root for 1181208 / 1438669 recognized words, accuracy = 82.10%
==================================================
--------------------------------------------------
Metrics for sanskrit_data
--------------------------------------------------
Recognized 1670698 / 1932518 words, accuracy = 86.45%
Correct root for 1375194 / 1670698 recognized words, accuracy = 82.31%
==================================================
--------------------------------------------------
Metrics for combined
--------------------------------------------------
Recognized 1692948 / 1932518 words, accuracy = 87.60%
Correct root for 1429996 / 1692948 recognized words, accuracy = 84.47%
==================================================
```

### Dependencies

Depends on dcs_wrapper python package for the data and openpyxl
for logging some results. All dependencies can be installed using
```pip install dcs_wrapper openpyxl progressbar2```

### TODO:
- Compute precision metrics as well

