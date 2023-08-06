# amba-event-stream

[![PyPI][]][1]

  [PyPI]: https://img.shields.io/pypi/v/amba-event-stream
  [1]: https://pypi.org/project/amba-event-stream/

The Amba Analysis Streams package is used as a Kafka connection wrapper to abstract from infrastructure implementation details by providing functions to connect to Kafka and PostgreSQL. It defines the event model used in the streaming platform and provides base consumer and producer classes. The package is implemented as a python package that is hosted on pypi.org, and documented with mkdocs.

The consumer and producer are capable of running in multiple processes to allow for parallel processing to better utilize modern CPUs. Both have built in monitoring capabilities: a counter shared by all processes is updated for each processed event. A thread running a function every few seconds is checking the counter and resetting it. If no data is processed over a defined period of time (meaning multiple consecutive check function runs), the container is restarted automatically by closing all python processed. This heart beat function ensures that even unforeseeable errors, such as container crashes or blockings are resolved by restarting the container and providing a clean system state. 

more Information can be found [here](https://github.com/ambalytics/amba-analysis-streams/blob/fce56afbd7d8207b847c270ffa2c6e025dcc1950/docs/Recognition-of-Scholarly-Publication-Trends-based-on-Social-Data-Stream-Processing_Lukas-Jesche.pdf)

# Installation

``` bash
pip install amba-event-stream
```

# Releasing

Releases are published automatically when a tag is pushed to GitHub.

``` bash
# Set next version number
export RELEASE=x.x.x

# Create tags
git commit --allow-empty -m "Release $RELEASE"
git tag -a $RELEASE -m "Version $RELEASE"

# Push
git push upstream --tags
```
