# GitHub Projects Manager - Burndown Chart Generator and Issues Creator

MIT License

Copyright (c) 2024 José Mendes

This project is available on 
[José Mendes GitHub Profile](https://github.com/josemendes03)

Permitted uses, modifications, and distribution of the software are governed by the terms of the MIT License.


## GitHub Issues Generator

This is a simple tool to generate a markdown file with the issues of a github project. It is written in Python and uses the requests library to interact with the GitHub API.

### Usage

#### 1. Enter Python Virtual Environment:

```bash
source myenv/bin/activate
```

#### 2. Get UserStories from RFP Doc in `requirements_reader.py`:

```bash
python3 1-requirements_reader.py
```

#### 3. Add Issues to GitHub Repository:

```bash
python3 2-add_issues.py
```

#### 4. Move Issues to Project Board:

This step is done manually by associating the issues to the project board.
At moment, the tool does not support this feature due to the GitHub API limitations.

##### Troubleshooting

If you have any issues with the tool, you can check if reached the GitHub API rate limit:

```bash
python3 check_api_requests_limit.py
```


#
## Burndown Chart Generator

This is a simple tool to generate burndown charts for a github project. It is written in Python and uses the matplotlib library to generate the charts.

### Usage

#### 1. Enter Python Virtual Environment:

```bash
source myenv/bin/activate
```

#### 2. Adjust Initial Data in `obtain_issues.py`:

```python
start_date = datetime(2024, 10, 28, tzinfo=timezone.utc)
```

#### 2.Obtain Issues CSV from Github:

```bash
python3 obtain_issues.py
```

#### 3. Generate Burndown Chart:

```bash
python3 generate_burndown_chart.py
```




