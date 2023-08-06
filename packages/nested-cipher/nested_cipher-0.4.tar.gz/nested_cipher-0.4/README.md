# NESTED CIPHER

**Easy and Simple Data Cipher**

```shell
pip install nested_cipher
```



---

## Available Method

> **b64**
>
> > **b64  :** Standard Base 64 Encode & Decode
> >
> > **ab64 :** All Base 64 Encode & Decode
> >
> > **mb64 :** Mid Base 64 Encode & Decode
> >
> > **eb64 :** Exclusive Base 64 Encode & Decode
> >
> > **lb64 :** Long Base 64 Encode & Decode
> >
> > **rb64 :** Reverse Base 64 Encode & Decode
> >
> > **rab64 :** Reverse All Base 64 Encode & Decode
> >
> > **rmb64 :** Reverse Mid Base 64 Encode & Decode
> >
> > **reb64 :** Reverse Exclusive Base 64 Encode & Decode
> >
> > **rlb64 :** Reverse Long Base 64 Encode & Decode

---

## Application

**_methods_ :** b64, ab64, mb64, eb64, lb64, rb64, rab64, rmb64, reb64, rlb64

**NOTE :** This Application __ISSUE__ With __BIG FILE__ For Big File Use Library and Handling File by your own. until Fixed this badly issue.

> **Positional**
>
> > **input :** Input data or File path
>
>  **Options**
>
> > **--time, -t :** Show Time To Done
> >
> > **--out, -O :** Path For Result File If You Want to Write to File.
> >
> > **--mode, -m :** Mode. Choose 'en', 'de'   **default :** 'en' encode
> >
> > **--type, -T :** Type Input Data. Choose 't', 'f'   **default :** 't' text
> >
> > **--method, -M :** Select Method. Choose **_methods_**   **default :** 'mb64'

---

## nested_cipher  Library

**Example**

> **Import :**
>
> change in `v0.4` see `changes.md`
>
> ```python
> import nested_cipher.b64
> ```
>
> **or**
>
> change in `v0.4` see `changes.md`
>
> ```python
> from nested_cipher.b64 import b64_encode, b64_decode
> ```

> **Encode :**
>
> ```python
> data = 'T3STSTR!NG'.encode('utf-8')
> b64_cipher = b64_encode(data)
> ```

> **Decode :**
>
> ```python
> data = 'VDNTVFNUUiFORw=='.encode('utf-8')
> decode_data = b64_decode(data)
> ```

---

## Use Application

[nested_cipher]: https://github.com/Class-Tooraj/nested_cipher	"nested_cipher in git hub"

**Base 64 URL SAFE**

> **Encode :**
>
> ```bash
> > py main.py Test -M b64
> ```
>
> ```bash
> b'VGVzdA=='
> ```
>
> 

> **Decode :**
>
> ```bash
> > py main.py VGVzdA== -M b64 -m de
> ```
>
> ```bash
> b'Test'
> ```



**File To Base 64 URL SAFE**

> **Encode :**
>
> ```bash
> > py main.py ./test.t -M b64 -T f -O ./test.txt
> ```

> **Decode :**
>
> ```bash
> > py main.py ./test.txt -m de -M b64 -T f -O ./test.t
> ```
>

---

author: **Tooraj Jahangiri**
version: **0.4**

