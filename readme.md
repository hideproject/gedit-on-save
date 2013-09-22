Gedit 3 On Save
===============================================

Plugin runs a command on save of document.


Installation
------------

Run script ```install.sh```:

```
./install.sh
```


Definition a new commands
-------------------------

Create a file with ```.json``` extension in plugin directory (default ```~/.local/share/gedit/plugins/gedit-hide-onsave```).

``` json
{
	"filepath-mask": [
		{
			"cmd": "command %file% %lang%",
			"active": "no"
		}
	],
	
	"*/composer.json": [
		{
			"cmd": "composer validate %file%",
			"active": "yes"
		}
	],
	
	"*.js": [
		{
			"cmd": "jshint %file%",
			"active": "yes"
		}
	],
}
```


License
-------

Copyright (c) 2013 Jan Pecha (http://janpecha.iunas.cz/) All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

-----------------

Author: [Jan Pecha](http://janpecha.iunas.cz), <janpecha@email.cz>
