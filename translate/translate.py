# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

def run_translate(text, source, target):
    # [START translate_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import translate

    # Instantiates a client
    translate_client = translate.Client()

    # Translates some text from source into target
    translation = translate_client.translate(
        text,
        source_language=source,
        target_language=target)

    # Return the Translated_Text
    return translation['translatedText']
    # [END translate_quickstart]


if __name__ == '__main__':
    run_quickstart(sys.argv[1], sys.argv[2], sys.argv[3])
