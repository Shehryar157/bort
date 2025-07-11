import os
from platform_utils.paths import module_path, is_frozen, embedded_data_path

if is_frozen():
    x86_path = os.path.join(embedded_data_path(), 'sound_lib', 'lib', 'x86')
    x64_path = os.path.join(embedded_data_path(), 'sound_lib', 'lib', 'x64')
else:
    x86_path = os.path.join(module_path(), '..', 'lib', 'x86')
    x64_path = os.path.join(module_path(), '..', 'lib', 'x64')
