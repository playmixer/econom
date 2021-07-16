import config from "../../../../config.json"

const API = `${config.subdirectory}/api/v0/`

const _response = async (method, url, data) => {
    const res = await fetch(API + url, {
        method,
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(data)
    })
        .then(res => {
            return res.json()
        })
    return res
}

export const post = async (url, data) => await _response('post', url, data)

export const get = async (url, data) => await _response('get', url, data)
