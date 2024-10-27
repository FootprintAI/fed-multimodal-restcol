# fed-multimodal-restcol
implement fed-multimodal with restcol

reference:
- fed-multimodal: https://github.com/usc-sail/fed-multimodal/tree/main
- restcol api: https://github.com/FootprintAI/restcol


#### setup steps
0. login reststore go get its auth token


1. use upload.py to upload dataset onto restcol

`cd fed_multimodal_restcol/trainer/run`

- upload img data and collect its document id

`python3 upload.py --collection_id=crisis-mmd --pkls ../../../data/img/dev.pkl ../../../data/img/test.pkl`

- upload text data and collect its document id

`python3 upload.py --collection_id=crisis-mmd --pkls ../../../data/text/dev.pkl ../../../data/text/test.pkl`

2. run server code with session id (consider each new session represents a new start), the server would be associated with two client (cid1, cid2)

```
python3 server.py --session_id=sid1 --client_ids cid1 cid2 --restcol_host=http://storage.demo01.footprint-ai.com

```

3. run client code with $sid and $client_id

```
client.py --session_id=sid1 --client_id=cid1 --dataset_collection_id=crisis-mmd --dataset_img_document_id=0192cca6-2a56-79fc-bfd7-ad30ca49bf66 --dataset_text_document_id=0192cca6-98e1-7c2a-9013-569adbcec9c8
```