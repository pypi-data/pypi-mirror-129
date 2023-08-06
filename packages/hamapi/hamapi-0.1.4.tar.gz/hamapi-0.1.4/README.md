HAM Systems API for Python
--------------------------

With this python package, you can easily access datalog data for your [HAM Systems](https://hamsystems.eu) devices.

You are free to use this code as you like and we are looking forward to seeing on what you achieve with our platform!

```
#!/usr/bin/env python3

import time, datetime
import math 

import hamapi

if __name__ == "__main__":
	# set you API key here
	ham = hamapi.hamapi(api_key='', server='hamsystems.eu')
	# unix timestamp of the start of data
	start = math.floor(time.time()-7*86400)
	# unix timestamp of the end of data
	end = math.floor(time.time()-86400)
	# step to smooth/average the data in seconds
	step = 2*60
	# get datalog data for device with serialno 12:204, from start to end with step
	data = ham.get_datalog_data("12:204", start, end)
	print(data)

	# fig, ax = plt.subplots()
	# ax.plot([datetime.datetime.utcfromtimestamp(d) for d in data['timestamp']], data['T'])
	# ax.grid()
	# plt.show()
```