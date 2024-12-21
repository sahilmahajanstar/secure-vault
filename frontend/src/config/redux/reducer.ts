import { combineReducers } from '@reduxjs/toolkit'
import fileReducer from '../../files/reducer/fileReducer'
import userReducer from '../../users/reducer/userReducer'

const rootReducer = combineReducers({
    user: userReducer,
    file: fileReducer,
})

export default rootReducer
