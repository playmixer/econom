import {createSlice} from '@reduxjs/toolkit'

const defaultAuthState = {
    isAuth: false,
    error: ''
}

const initialAuthState = JSON.parse(window.localStorage.getItem('auth')) || defaultAuthState

const saveStore = (data) => localStorage.setItem('auth', JSON.stringify({...data}))
const removeStore = () => localStorage.removeItem('auth')

export const userSlice = createSlice({
    name: 'user',
    initialState: {
        ...initialAuthState
    },
    reducers: {
        store: (state) => {
            saveStore(state)
        },
        userInfo: (state, action) => {
            state = {
                ...state,
                ...action.payload,
            }
            saveStore(state)
            return state
        },
        signIn: (state) => {
            state = {
                ...state,
                isAuth: true
            }
            return state
        },
        logout: (state) => {
            state.isAuth = false
            removeStore()
            return state
        },
        setError: (state, action) => {
            state.error = action.payload
        }
    },
})

// Action creators are generated for each case reducer function
export const {signIn, logout, setError, store, userInfo} = userSlice.actions

export default userSlice.reducer
