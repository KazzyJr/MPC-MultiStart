# MPC-MultiStart
`Start Offset Videos in tandem`

A tool that allows you to start synchronized MPC-HC video players with or without offset.

### The Config

The `config.json` object is used for adjusting the run parameters of the tool.
* `base_command` refers to the base command that is used to spawn an MPC-HC instance;
* `first_argument` refers to the start position indicator;
* `second_argument` refers to the MPC-HC target instance toggle;
* `path_to_movies_json` refers to the JSON object which contains the file-start_time mapping;
* `time_offset` refers to the time added (positive integer) or subtracted (negative integer) from all the times of the 
  yet to be launched movies;
* `quiet` refers to whether the application prints or not;
* `dry_run` refers to the application only printing the end commands;

### The input JSON

The `movies_template.json` object is used for specifying a path to time mapping.
```json
{
  "path/to/file1.mp4": "00:01:15",
  "path/to/file2.mp4": "00:02:15",
  "path/to/file3.mp4": "00:03:30"
}
```
The files in the mapping will be started simultaneously at the times indicated (if the configured offset is 0), or 
using the calculated offset (if the configured offset is non-0)