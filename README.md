# fed-multimodal-restcol
implement fed-multimodal with restcol

reference:
- fed-multimodal: https://github.com/usc-sail/fed-multimodal/tree/main
- restcol api: https://github.com/FootprintAI/restcol

#### python path

```
export PYTHONPATH = $(PWD)

to allow python search path started from current dir.
```

#### setup steps

1. upload dataset

```
// configure s3 storage endpoint

export STORAGE_ENDPOINT=<s3-endpoint>
export STORAGE_BUCKET_NAME=<bucket-name>
export STORAGE_ACCESS_KEY=<access-key>
export STORAGE_ACCESS_SECRET=<access-secret>
```

// use upload.py script to upload img dataset
```
python3 fed_multimodal_restcol/trainer/run/upload.py \
  --pkls ../../../data/img/dev.pkl ../../../data/img/test.pkl \
  --restcol_collection_id=crisis-mmd \
  --restcol_endpoint=<endpoint> \
  --restcol_authtoken=<authtoken> \
  --restcol_projectid=<projectid>

>> docid: 0192d96d-778d-7ef4-b15b-03063b0dc890

// use upload.py script to upload text dataset

python3 fed_multimodal_restcol/trainer/run/upload.py \
  --pkls ../../../data/text/dev.pkl ../../../data/text/test.pkl \
  --restcol_collection_id=crisis-mmd \
  --restcol_endpoint=<endpoint> \
  --restcol_authtoken=<authtoken> \
  --restcol_projectid=<projectid>

>> docid: docid: 0192d96e-ee67-78fb-8359-388ec4eff8d2
```

2. run server code with session id (consider each new session represents a new start), the server would be associated with two client (cid1, cid2)

```
python3 fed_multimodal_restcol/trainer/run/server.py \
  --session_id=sid1 \
  --client_ids cid1 cid2 \
  --restcol_host=<endpoint> \
  --restcol_projectid=<projectid> \
  --restcol_authtoken=<authtoken>

```

3. run client code with $sid and $client_id

```
python3 fed_multimodal_restcol/trainer/run/client.py \
  --session_id=sid1 \
  --client_id=cid1 \
  --dataset_collection_id=crisis-mmd \
  --dataset_img_document_id=0192d96d-778d-7ef4-b15b-03063b0dc890 \
  --dataset_text_document_id=0192d96e-ee67-78fb-8359-388ec4eff8d2
```
