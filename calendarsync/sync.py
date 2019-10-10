from xml.etree.ElementTree import fromstring

HTML = """
<table class="details" border="0" cellpadding="5" cellspacing="2" width="95%">
  <tr valign="top">
    <th>Tests</th>
    <th>Failures</th>
    <th>Success Rate</th>
    <th>Average Time</th>
    <th>Min Time</th>
    <th>Max Time</th>
  </tr>
  <tr valign="top" class="Failure">
    <td>103</td>
    <td>24</td>
    <td>76.70%</td>
    <td>71 ms</td>
    <td>0 ms</td>
    <td>829 ms</td>
  </tr>
  <tr valign="top" class="whatever">
    <td>A</td>
    <td>B</td>
    <td>C</td>
    <td>D</td>
    <td>E</td>
    <td>F</td>
  </tr>
</table>"""

tree = fromstring(HTML)
rows = tree.findall("tr")
headrow = rows[0]
datarows = rows[1:]

for num, h in enumerate(headrow):
    data = ", ".join([row[num].text for row in datarows])
    print ("{0:<16}: {1}".format(h.text, data))