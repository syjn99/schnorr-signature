# Schnorr Signature Scheme written in Python

> Homework from KAIST EE488 (Introduction to Cryptography - [Schnorr Signature Scheme written in Python](#schnorr-signature-scheme-written-in-python)

- [Schnorr Signature Scheme written in Python](#schnorr-signature-scheme-written-in-python)
  - [Setup](#setup)
  - [Available Commands](#available-commands)
    - [Test with test vectors](#test-with-test-vectors)
  - [Implementation Details](#implementation-details)
    - [Dependencies](#dependencies)
    - [JSON-formatted](#json-formatted)
    - [Signature](#signature)
  - [Solutions to Questions](#solutions-to-questions)
    - [Question 2: $L, N$ less than $20$](#question-2-l-n-less-than-20)
  - [Question 3: $L, N$ less than $64$](#question-3-l-n-less-than-64)
    - [Question 5: $(L, N) = (2048, 256)$](#question-5-l-n--2048-256)
    - [Question 7: Parameter Generation for $(L, N) = (2048, 256)$](#question-7-parameter-generation-for-l-n--2048-256)


Simple Python implementation of Schnorr Signature Scheme using [gmpy2](https://gmpy2.readthedocs.io/en/latest/).

## Setup

1. This project uses [uv](https://docs.astral.sh/uv/) as a project manager. ([Installation guide](https://docs.astral.sh/uv/#installation))
2. Install dependencies with:

```sh
$ uv sync
```

## Available Commands

```sh
$ uv run main.py -h

usage: main.py [-h] {paramgen,keygen,sign,verify,bench,test} ...

Python implementation of Schnorr signature scheme

positional arguments:
  {paramgen,keygen,sign,verify,bench,test}
    paramgen            Generate public parameters for Schnorr signature scheme
    keygen              Generate keypair for Schnorr signature scheme
    sign                Sign a message using the Schnorr signature scheme
    verify              Verify a Schnorr signature
    bench               Benchmark the Schnorr signature scheme
    test                Run tests for the Schnorr signature scheme with given test vectors

optional arguments:
  -h, --help            show this help message and exit
```

For detailed arguments, refer to the `help` for each command:

```sh
$ uv run main.py {paramgen,keygen,sign,verify,bench,test} -h
```

- **`paramgen`**: Generate public parameters and save it to given path(`--output`) as a JSON format.
  - To generate a fresh parameters, specify $L$(`--l`) and $N$(`--n`) which indicates bit length of $p$ and $q$ respectively.
  - To use precomputed parameters, specify $p$(`--p`), $q$(`--q`), and $g$(`--g`). After basic validation, it will save the parameters as a JSON formatted file.
- **`keygen`**: Generate a key pair for given public parameters(`--param_file`). Save the key pair to given path(`--output`) as a JSON format.
  - To use precomputed key pair, specify $x$(`--x`) and $y$(`--y`). After basic validation, it will save the key pair as a JSON formatted file.
- **`sign`**: Sign a given message(`--m`) with given public parameters(`--param_file`) and key pair(`--key_file`). Save the signature to given path(`--output`) as a JSON format.
  - Specifing the random number $k$(`--k`) is available.
- **`verify`**: Verify a given signature(`--signature_file`).
- **`bench`**: Walk through the entire cycle: the public parameter generation, the key generation, the signing algorithm, and the verification algorithm. The last line of the result shows the total elapsed time.
  - You can either 1) specify $L$ and $N$ to generate fresh public parameters, or 2) use pre-computed parameters.
  - See the results at [`benchmarks`](./benchmarks/) directory.

### Test with test vectors

```sh
$ sh test_vectors.sh
```

This command will run all the test vectors using `uv run main.py test` command.

## Implementation Details

### Dependencies

This project only depends on [gmpy2](https://gmpy2.readthedocs.io/en/latest/) for primality test(`is_strong_bpsw_prp`) as following: 

```python
# Use Baillie–PSW primality test that is reliable, and also provided by gmpy2.
# Reference: https://en.wikipedia.org/wiki/Baillie%E2%80%93PSW_primality_test
def is_prime(n: int) -> bool:
    return gmpy2.is_strong_bpsw_prp(n)
```

Although there are numerous methods to test a primality of the given number(See [Wikipedia](https://en.wikipedia.org/wiki/Primality_test)), I selected Baillie–PSW primality test because:

1. This project should handle a real-world parameter ($(L, N) = (2048, 256)$). Using trial division or other method will slow the parameter generation.
2. `gmpy2` provides the test function.

### JSON-formatted

All output and input are serialized/deserailized into JSON which makes running each step easier. You can follow the life cycle of signature with the following commands:

```sh
# Public Parameter Generation
uv run main.py paramgen --l 20 --n 10 --output ./param.json

# Key Generation
uv run main.py keygen --param_file ./param.json --output ./keypair.json

# Sign a message
uv run main.py sign --param_file ./param.json --key_file ./keypair.json --message abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq --output ./signature.json

# Verify the signature
uv run main.py verify --signature_file ./signature.json
```

### Signature

```json
{
  "s": 794,
  "e": 619,
  "m": "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
  "public_key": 594448,
  "param": {
    "p": 687523,
    "q": 947,
    "g": 126172
  }
}
```

A container `Signature` contains an additional information other than `s` and `e` in order to provide `Signature.verify()` method to the verifier.



## Solutions to Questions

### Question 2: $L, N$ less than $20$

```sh
uv run main.py bench --l 20 --n 10
```

This command will print out all the steps like:

```plaintext
Benchmarking the Schnorr signature scheme...
Generating new parameters...
Public Parameters:
 p: 893261
 q: 757
 g: 554190

Keypair generation...
Key Pair:
 Public Key: 404649
 Secret Key: 729

Signing the message: 5OUHepEf89UnTf3EjUzuSJ6c99QNruvbx3rpicm8u5WN1NfVUN
Signature:
  s: 221
  e: 1015
  m: 5OUHepEf89UnTf3EjUzuSJ6c99QNruvbx3rpicm8u5WN1NfVUN
  public_key: 404649
  Public Parameters:
    p: 893261
    q: 757
    g: 554190

Verifying the signature...
Signature is valid.
Benchmarking completed in 0.00 seconds.
```

## Question 3: $L, N$ less than $64$

```sh
uv run main.py bench --l 64 --n 32
```

This command will print out all the steps like:

```plaintext
Benchmarking the Schnorr signature scheme...
Generating new parameters...
Public Parameters:
 p: 12728329895042105159
 q: 3222643289
 g: 10402980446840271522

Keypair generation...
Key Pair:
 Public Key: 479131200948880331
 Secret Key: 788761707

Signing the message: 8vh6i32JIWa66ZWGgfityNo2jrMoHtiNtYt5rc3s4uwSthaAXe
Signature:
  s: 2484663133
  e: 1704959853
  m: 8vh6i32JIWa66ZWGgfityNo2jrMoHtiNtYt5rc3s4uwSthaAXe
  public_key: 479131200948880331
  Public Parameters:
    p: 12728329895042105159
    q: 3222643289
    g: 10402980446840271522

Verifying the signature...
Signature is valid.
Benchmarking completed in 0.00 seconds.
```

### Question 5: $(L, N) = (2048, 256)$

```sh
uv run main.py bench --l 2048 --n 256
```

```plaintext
Benchmarking the Schnorr signature scheme...
Generating new parameters...
Public Parameters:
 p: 28239271561534943181831927856196159568624043591786947377985130625384419146068111466400100377937662746153512000000601983402625116659211415499440256183973180000182189027370230650615173607036603830208040519119013356141712095187377786447004466099457806554442686385599845205064179154308870238464963147092902199135558717499468778101498702156579067750221531941769084754585775270009618360775537848310241255095044312081221084323842293140504455862364281573282165831265899713121938509654890522018544629790085992655796409304071570992155938333064231170585870920880858502341317820553292162186425666327450009370605956856390389812189
 q: 96156237584929751988686633910293889103912331797739647847087355696806838980591
 g: 23219442326365051130599656361236834964488606100414670692323628176428974301414082343513812514672142064354348989944931255795940739788287931362430411126797756072436393837269125667018711947692379785323455479416743222744501194974524688246067726479637101884708649885126675469281231964053521873927035611074137183563634503448126030247903202646133542642023274577927028921693417252526447703263555157653254477749638749084731125982680978155198300160082128869198792902894152945311445955644076533043467223250256174089443365520730995406272693330423009093197941817221793752411548520277765278179324503713469834215710991598082782094807

Keypair generation...
Key Pair:
 Public Key: 1430832732822485368800510332776856440807499550301571236222851208489947986017562889925655359062025410743855460058907311005460191029629700778631332443720334627589028623344085106526009126558986455417387091433712280549191886561866711963972218755221198417356885504686753401970916615278258924355836628629149744206820439885581681118103039304296799757740415570087753001959563447964708354017788770495144878543165926286885809220639370571717067564116138940856170360387227026198334409140952826842019128515063949338683379561856151253485994470389865179620823789046307220288892968478670763618473271130369335748776509252992514228226
 Secret Key: 31609469342464981079817722711619054868265190811333135812047709575916170260928

Signing the message: vrHLekdhOoFqcqabepfsbf0owqEJswsovPaLMfmxuOJo1jQ5u2
Signature:
  s: 7730079348864833048289859539690404836186716922826629601809383550217984815335
  e: 44038700238196427486401186565689489290362735184536780399563976286692445033594
  m: vrHLekdhOoFqcqabepfsbf0owqEJswsovPaLMfmxuOJo1jQ5u2
  public_key: 1430832732822485368800510332776856440807499550301571236222851208489947986017562889925655359062025410743855460058907311005460191029629700778631332443720334627589028623344085106526009126558986455417387091433712280549191886561866711963972218755221198417356885504686753401970916615278258924355836628629149744206820439885581681118103039304296799757740415570087753001959563447964708354017788770495144878543165926286885809220639370571717067564116138940856170360387227026198334409140952826842019128515063949338683379561856151253485994470389865179620823789046307220288892968478670763618473271130369335748776509252992514228226
  Public Parameters:
    p: 28239271561534943181831927856196159568624043591786947377985130625384419146068111466400100377937662746153512000000601983402625116659211415499440256183973180000182189027370230650615173607036603830208040519119013356141712095187377786447004466099457806554442686385599845205064179154308870238464963147092902199135558717499468778101498702156579067750221531941769084754585775270009618360775537848310241255095044312081221084323842293140504455862364281573282165831265899713121938509654890522018544629790085992655796409304071570992155938333064231170585870920880858502341317820553292162186425666327450009370605956856390389812189
    q: 96156237584929751988686633910293889103912331797739647847087355696806838980591
    g: 23219442326365051130599656361236834964488606100414670692323628176428974301414082343513812514672142064354348989944931255795940739788287931362430411126797756072436393837269125667018711947692379785323455479416743222744501194974524688246067726479637101884708649885126675469281231964053521873927035611074137183563634503448126030247903202646133542642023274577927028921693417252526447703263555157653254477749638749084731125982680978155198300160082128869198792902894152945311445955644076533043467223250256174089443365520730995406272693330423009093197941817221793752411548520277765278179324503713469834215710991598082782094807

Verifying the signature...
Signature is valid.
Benchmarking completed in 0.15 seconds.
```

### Question 7: Parameter Generation for $(L, N) = (2048, 256)$

[Question 6](#question-5-l-n--2048-256) contains generating fresh public parameters, but to be more clear, I added a `--validate` flag for `paramgen`. It will check(See validation logic at [`paramgen.py`](./paramgen.py)):

1. Is $q \mid (p-1)$?
2. Is $p$ and $q$ are prime?
3. Is the order of $g$ equal to $q$?

To run the command, add `--validate` as follow:

```sh
$ uv run main.py paramgen --l 2048 --n 256 --validate true
```

This will print like:

```plaintext
Public parameters saved to params/param.json
Validating the parameters...
Parameters are valid.
```