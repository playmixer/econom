import * as userReducer from '../reducers/user'
import * as apiAuth from "../../api/auth";


export const signIn = ({username, password}) => (dispatch) => {
    apiAuth.signIn({username, password})
        .then(res => {
            if (res.Ok) {
                dispatch(userReducer.signIn())
                dispatch(userReducer.userInfo(res.Data))
            } else {
                dispatch(userReducer.logout())
            }
        })
        .catch(err => dispatch(userReducer.setError(err)))
}

export const logout = () => (dispatch) => {
    console.log('logout')
    apiAuth.logout()
        .then(res => res)
        .finally(() => {
            dispatch(userReducer.logout())
        })
}

export const source = () => (dispatch) => {
    apiAuth.source()
        .then(res => {
            console.log('source', res)
            if (res.Ok) {
                if (res.Data.isAuth)
                    dispatch(userReducer.userInfo({
                        isAuth: res.Data.isAuth,
                        model: res.Data.model
                    }))
                else
                    dispatch(logout())
            }
        })
}
