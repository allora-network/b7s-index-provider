# Deprecation Notice

🚨 **This repository is deprecated and no longer maintained.** 🚨

This project is no longer actively developed or maintained. We recommend using [allora-offchain-node](https://github.com/allora-network/allora-offchain-node) as a replacement.

## Why is this project deprecated?

The architecture has been improved and simplified, and heads and workers supported by this project are are not compatible. 


## What should you do?

- **Switch to allora-offchain-node**: [allora-offchain-node](https://github.com/allora-network/allora-offchain-node)
- **Read the Docs**: Refer to docs on architecture (and workers specifically) on [Allora Network Docs](https://docs.allora.network/).


Thank you to everyone who contributed to this project.



# Index 

This is an application packaged for being run on the Allora Network.
It is an example of a setup for running an Allora Network node for providing index prices.

# Components

* **worker**: The node that will respond to requests from the Allora Network heads.
* **head**: An Allora Network head node. This is not required for running your node in the Allora Network, but it will help for testing your node emulating a network.

When a request is made to the head, it relays this request to a number of workers associated with this head. The request specifies a function to run which will execute a wasm code that will call the `main.py` file in the worker. 
This code will get the index price from Upshot API, and returns this value to the `head`, which prepares the response from all of its nodes and sends it back to the requestor.


# docker-compose
A full working example is provided in `docker-compose.yml`.

## Structure
There is a docker-compose.yml provided that sets up one head node and one worker node.

**NOTE:** Bear in mind, for simplicity, current docker-compose file runs containers from root user. If you going to use docker-compose.yml for production environemnts, consider commenting `user: 0:0` - to run it from non-root user, and you will need to provision writable volume to store databases.

## Dependencies
- Have an available image of the `allora-inference-base` , and reference it as a base on the `FROM` of the `Dockerfile`.
- Create a set of keys in the `keys` directory for your head and worker, and use them in the head and worker configuration(volume mapping already provided in `docker-compose.yml` file). If no keys are specified in the volumes, new keys are created. However, the worker will need to specify the `peer_id` of the head for defining it as a `BOOT_NODES`. You can bring head up first, get the key from the container, then use it in the `BOOT_NODES`. For more information, see [how to generate keys](https://github.com/allora-network/basic-coin-prediction-node#docker-compose-setup).
- Provide a valid `UPSHOT_API_TOKEN` env var inside the `node/.env` file. You can [create one here](https://developer.upshot.xyz/).

## Run 

Once this is set up, run `docker compose up`


Once both nodes are up, a function can be tested by hitting:

```
curl --location 'http://localhost:6000/api/v1/functions/execute' \
--header 'Accept: application/json, text/plain, */*' \
--header 'Content-Type: application/json;charset=UTF-8' \
--data \
'{
    "function_id": "bafybeigpiwl3o73zvvl6dxdqu7zqcub5mhg65jiky2xqb4rdhfmikswzqm",
    "method": "allora-inference-function.wasm",
    "topic": "2",
    "config": {
        "env_vars": [
            {
                "name": "BLS_REQUEST_PATH",
                "value": "/api"
            },
            {
                "name": "ALLORA_ARG_PARAMS",
                "value": "yuga"
            }
        ],
        "number_of_nodes": 1
    }
}'

```
And the response:
```
{
  "code": "200",
  "request_id": "f5b8944d-2177-4005-8476-7319cd4045f0",
  "results": [
    {
      "result": {
        "stdout": "{\"value\": \"46071353120000000000\"}\n\n",
        "stderr": "",
        "exit_code": 0
      },
      "peers": [
        "12D3KooWN6vwWEbMASaVYxJ257XLF3aLjktfwvxuaRFT99w2omhq"
      ],
      "frequency": 100
    }
  ],
  "cluster": {
    "peers": [
      "12D3KooWN6vwWEbMASaVYxJ257XLF3aLjktfwvxuaRFT99w2omhq"
    ]
  }
}
```

## Connecting to the Allora network

In order to connect to an Allora network to provide inferences, both the head and the worker need to register against it.
The following optional flags are used in the `command:` section of the `docker-compose.yml` file to define the connectivity with the Allora network.

```
--allora-chain-key-name=index-provider  # your local key name in your keyring
--allora-chain-restore-mnemonic='pet sock excess ...'  # your node's Allora address mnemonic
--allora-node-rpc-address=  # RPC address of a node in the chain
--allora-chain-topic-id=  # The topic id from the chain that you want to provide predictions for
```
In order for the nodes to register with the chain, a funded address is needed first.
If these flags are not provided, the nodes will not register to the appchain and will not attempt to connect to the appchain.


## GitHub actions

### build_push_ecr - Build and push docker images to ECR registry

* Name of the ECR registry is the same as the GitHub repo name.
* The GH action will build a new docker image from PRs and pushes to the main branch.
* **All images** tagged with `$GIT_SHA` and `dev-latest` tags.
* If image built from main branch, then it will also have tagged with `latest` tag.

