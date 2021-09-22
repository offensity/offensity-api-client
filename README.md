# Offensity API Client

This python3 script makes use of our API, allowing to export scanprofiles, reports and issue data.

### Authentication
A token based authentication is used to authenticate clients. 
Tokens can be obtained in your account settings (see [API Tokens](https://staging-reporting.offensity.com/accounts/apitokens/))

### Ratelimit
The API is rate limited to 100 requests per second per user.

### Quick start
```
git clone https://github.com/offensity/offensity-api-client
cd offensity-api-client
python3 -m pip install -r requirements.txt
python3 example.py --token <YOUR_OFFENSITY_API_TOKEN> --verbose
```

### Files
The core logic lies within the `offensity_api_client.py` script and `example.py` just demonstrates
how to initialize it and make use of the methods.

### Methods overview
<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>ReturnType</th>
      <th>Fields</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>scanprofiles_list</code></td>
      <td>iterable[dict]</td>
      <td>
        <ul>
          <li><code>is_enabled [bool]</code>(optional)</li>
          <ul>
            <li><code>None</code> Both enabled & disabled (default)</li>
            <li><code>True</code> Only enabled scanprofiles</li>
            <li><code>None</code> Only disabled scanprofiles</li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>scanprofile_details</code></td>
      <td>dict</td>
      <td>
        <ul>
          <li><code>scanprofile_id [str]</code>(mandatory)</li>
          <ul>
            <li><code>scanprofile_json.get("id")</code></li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>report_list</code></td>
      <td>iterable[dict]</td>
      <td>
        <ul>
          <li><code>status [str]</code>(optional)</li>
          <ul>
            <li><code>started</code> Scan in progress</li>
            <li><code>cancelled</code> Scan was cancelled</li>
            <li><code>success</code> Scan finished (default)</li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>report_list_for_scanprofile</code></td>
      <td>iterable[dict]</td>
      <td>
        <ul>
          <li><code>scanprofile_id [str]</code>(mandatory)</li>
          <ul>
            <li><code>scanprofile_json.get("id")</code></li>
          </ul>
            <br>
          <li><code>status [str]</code>(optional)</li>
          <ul>
            <li><code>started</code> Scan in progress</li>
            <li><code>cancelled</code> Scan was cancelled</li>
            <li><code>success</code> Scan finished (default)</li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>latest_report_for_scanprofile</code></td>
      <td>dict</td>
      <td>
        <ul>
          <li><code>scanprofile_id [str]</code>(mandatory)</li>
          <ul>
            <li><code>scanprofile_json.get("id")</code></li>
          </ul>
            <br>
          <li><code>status [str]</code>(optional)</li>
          <ul>
            <li><code>started</code> Scan in progress</li>
            <li><code>cancelled</code> Scan was cancelled</li>
            <li><code>success</code> Scan finished (default)</li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>report_details</code></td>
      <td>dict</td>
      <td>
        <ul>
          <li><code>report_id [str]</code>(mandatory)</li>
          <ul>
            <li><code>report_json.get("id")</code></li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>issues</code></td>
      <td>dict</td>
      <td>
        <ul>
          <li><code>report_id [str]</code>(mandatory)</li>
          <ul>
            <li><code>report_json.get("id")</code></li>
          </ul>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>infrastructure_data</code></td>
      <td>iterable[dict]</td>
      <td>
        <ul>
          <li><code>report_id [str]</code>(mandatory)</li>
          <ul>
            <li><code>report_json.get("id")</code></li>
          </ul>
            <br>
          <li><code>query [str]</code>(optional)</li>
          <ul>
                <li><code>ip</code></li>
                <li><code>subdomain</code></li>
                <li><code>port</code></li>
                <li><code>service</code></li>
                <li><code>version</code></li>
                <li><code>webtech</code></li>
                <li><code>issues</code></li>
                <li><code>risk</code></li>
                <li><code>statuscode</code></li>
                <br>
          </ul>
          <li>query examples:</li>
            <ul>
                <li><code>"ip:127.0.0.1" | "ip:127.0.0.*" | "ip:127.0.0.1/24"</code></li>
                <li><code>"port:21" | "port:53/tcp" | "port:53/udp"</code></li>
                <li><code>"service:*http*" | "service:ssl/http"</code></li>
                <li><code>"subdomain:www.example.com" | "subdomain:*dev*"</code></li>
                <li><code>"version:nginx*" | "version:'Apache httpd'</code></li>
                <li><code>"webtech:Django" | "webtech:Word*"</code></li>
                <li><code>"issues:SSL" | "issues:'SQL Injection'"</code></li>
                <li><code>"risk:critical" | "risk:low"</code></li>
                <li><code>"statuscode:200" | "statuscode:500" | "statuscode:404"</code></li>
            </ul>
        </ul>
      </td>
    </tr>
  </tbody>
</table>