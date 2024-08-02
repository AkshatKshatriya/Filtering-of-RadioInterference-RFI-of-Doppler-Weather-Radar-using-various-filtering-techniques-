# Filtering of RadioInterference (RFI) of Doppler Weather Radar data using various filtering techniques
This project explores various filtering techniques to mitigate Radio Frequency Interference (RFI) in Doppler Weather Radar (DWR) data. The aim is to evaluate the effectiveness of different filters and to identify the best approach for reducing RFI while preserving the integrity of the radar data.

# Project Overview

Doppler Weather Radar is an essential tool for meteorological observations, but they are often affected by Radio Frequency Interference (RFI) which can degrade the quality of the data. This project implements and compares three different filtering techniques:
1. Threshold Filtering
2. Median Filtering
3. Wiener Filtering

# Conclusions
- Threshold Filtering: A simple and fast method but not very effective in preserving data integrity.
- Median Filtering: Better at preserving edges but can still leave some RFI artifacts.
- Wiener Filtering: Performed better than threshold and median filters but still not optimal.

The study concludes that while the Wiener filter provides better results than the other two methods, it is not the best solution. Further work is required, particularly using machine learning models to achieve the least possible error in filtering RFI from DWR data.

