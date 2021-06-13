import {post, get} from './request'

export const signIn = async ({username, password}) => {
    return await post('auth/signin', {
        username,
        password
    })
}

export const logout = async () => {
    return await get('auth/logout')
}

export const source = async () => {
    return await get('auth/source')
}
