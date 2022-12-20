import os
import numpy as np
import pandas as pd
import json
from collections import Counter
import importlib
import pubtator

importlib.reload(pubtator)

input_path = "../1.Search/output/Bactology/"
output_path = "output/Bactology/"
pubtator.pubtator(input_path, output_path)