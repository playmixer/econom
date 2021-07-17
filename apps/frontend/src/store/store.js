import { configureStore } from '@reduxjs/toolkit'
import userReducer from './reducers/user'
import economReducer from './reducers/econom'

export default configureStore({
  reducer: {
    user: userReducer,
    econom: economReducer
  },
})
