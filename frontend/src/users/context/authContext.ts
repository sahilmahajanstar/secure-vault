import { Dispatch, createContext, useContext, useReducer } from 'react'
import { PayloadAction, UnknownAction, createSlice } from '@reduxjs/toolkit'

import { User } from '../type/user'

export interface AuthContextState {
    token: string | null
    loading: boolean
    user: User | null
}

const initialState: AuthContextState = {
    token: null,
    loading: true,
    user: null,
}

const authReducer = createSlice({
    name: 'authContext',
    initialState,
    reducers: {
        setUser: (
            state: AuthContextState,
            action: PayloadAction<{ user: User }>,
        ) => {
            state.user = action.payload.user
            state.loading = false
        },
        setLoading: (
            state: AuthContextState,
            action: PayloadAction<boolean>,
        ) => {
            state.loading = action.payload
        },
    },
})

export const useAuthReducer = () => {
    return useReducer(authReducer.reducer, initialState)
}

export const authContextActions = authReducer.actions

// to share the state and dispatch between components. THis is local redux store

const AuthContext = createContext<{
    state: AuthContextState
    dispatch: Dispatch<UnknownAction>
}>({ state: initialState, dispatch: () => {} })

export const useAuthContext = () => useContext(AuthContext)
export default AuthContext
