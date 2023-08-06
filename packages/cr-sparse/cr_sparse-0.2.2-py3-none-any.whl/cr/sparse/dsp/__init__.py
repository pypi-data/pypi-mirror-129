# Copyright 2021 CR.Sparse Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Signal Processing Utilities
"""

# pylint: disable=W0611


from cr.sparse._src.dsp.dct import (
    dct,
    idct,
    orthonormal_dct,
    orthonormal_idct
)


from cr.sparse._src.dsp.wht import (
    fwht,
)

from cr.sparse._src.dsp.synthetic_signals import (
    time_values,
)
