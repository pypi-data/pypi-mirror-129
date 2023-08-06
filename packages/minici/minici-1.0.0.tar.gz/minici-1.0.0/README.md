# MiniCI
## A small tool to make the life of programmers easier

When programming especially small applications iteratively, the overead of e.g., compiling and executing the application again and again can be very annoying.
MiniCI is intended to ease the life of a developer in such situations.
Setup your MiniCI configuration as a yaml file and execute minici with that configuration file. MiniCI will watch your configured files and automatically act upon file changes.
This way, e.g., a compiler can be automatically started as soon as you safe your source with a shortcut and the updated executable is executed when the compilation finishes without errors (example configuration for this can be found [here]).

# Installation and Usage

### Clone this repository and use pip to install the executable.
```bash
pip3 install minici
```

### Create a configuration file for minici

```
#minici-config.yml
observers:
    - files:
        - helloworld.cpp
      on_modify_triggers:
        - compile_helloworld

    - file: helloworld2.cpp
      on_modify_trigger: compile_helloworld2

processes:
    - trigger_signals:
        - compile_helloworld
      command: g++ helloworld.cpp -o helloworld
      on_success_triggers:
        - execute_helloworld

    - trigger_signal: compile_helloworld2
      command: g++ helloworld2.cpp -o helloworld

    - trigger_signals:
        - execute_helloworld
      command: ./helloworld
```

### Finally, simply execute 'minici' with a configuration file as argument.
(The executable might get installed into `~/.local/bin`. Install with sudo to install minici system wide)
```bash
minici <minici-config.yml>
```

# Future

### Updates and Improvements

I created this application to fit my needs, hence I will update it as soon as I found a bug or desire new featues.
I am open for any feedback or criticism.
If you find a bug or have suggestions, contact me and therefore help improve MiniCI.
Feel free to contact me via mail (anthony.zimmermann@protonmail.com) or open an issue if you like.

# License

BSD-3-Clause:

Copyright 2021, Anthony Zimmermann

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
