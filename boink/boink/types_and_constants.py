from typing import TypeAlias, Any

### Types

Config: TypeAlias = dict[str, Any]
Path: TypeAlias = str
DirName: TypeAlias = str
FileName: TypeAlias = str

### Constants

# Root config file/dir that must exist
ROOT_CONFIG_PATH_RE = re.compile(r"^\.boink(?:\.ya?ml)?$")

# Additional config for current directory
CONFIG_PATH_RE = re.compile(r"^\.config(?:\.ya?ml)?$")

# Only files that match this pattern will be published
CONTENT_FILE_RE = re.compile(r"\.md$")
