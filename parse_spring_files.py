#!/usr/bin/env python
import glob
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
import pickle

data = []
for file in glob.glob('/Users/michaesm/Documents/dev/repos/oceanobservatories/dataset-spring/res/spring/*.xml'):
    spring = os.path.basename(file)
    with open(file) as f:
        soup = BeautifulSoup(f, 'lxml')
        for route in soup.find_all('route'):
            uframe_route = re.search(r'\:queue:(.*)\?', route.find('from').get('uri')).group(1)
            uframe_id = route.find('bean').get('ref')
            driver = (soup.find(id=uframe_id).find(index='2').get('value'))
            data.append((spring, uframe_route , driver))

df = pd.DataFrame(data, columns=['spring', 'uframe_route', 'driver'])
df.to_csv(os.path.join(os.getcwd(), 'uframe_routes.csv'), index=False)

ingest_dict = {}
for row in df.itertuples():
    ingest_dict[row.uframe_route] = driver

with open(os.path.join(os.getcwd(), 'uframe_routes.pkl'), 'wb') as f:
    pickle.dump(ingest_dict, f)
