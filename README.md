# reexpose

Expose an authenticated HTTP endpoint on localhost as an unauthenticated one.

Built for Plex Podcasts to connect to premium podcast feeds.

## Installation & running

```
git clone https://github.com/jeffcasavant/reexpose.git
cd reexpose
pip install .
```

This will put ReExpose on your path.  Then, copy `config_example.yaml` to
`config.yaml` and edit it to your liking.  When you're ready:

```
reexpose path/to/config.yaml
```

ReExpose will make the endpoint available on localhost at port 5000 by default.
