import { PayloadAction, createSlice } from '@reduxjs/toolkit'
import { Profile, User } from '../type/user'

interface UserState {
    user: User | null
    token: string | null
    refreshToken: string | null
    loading: boolean
    isAuthenticated: boolean
    profile: Profile | null
}

const initialState: UserState = {
    user: null,
    token: null,
    refreshToken: null,
    loading: false,
    isAuthenticated: false,
    profile: null,
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        clearUser: (state: UserState) => {
            state.user = null
        },
        setUserAndProfile: (
            state: UserState,
            action: PayloadAction<{ user: User; profile: Profile }>,
        ) => {
            state.user = action.payload.user
            state.profile = action.payload.profile
        },
        setUserInfo: (
            state: UserState,
            action: PayloadAction<{
                user: User
                token: string
                refreshToken: string
            }>,
        ) => {
            state.user = action.payload.user
            state.token = action.payload.token
            state.refreshToken = action.payload.refreshToken
            state.isAuthenticated = true
            localStorage.setItem('token', action.payload.token)
            localStorage.setItem('refreshToken', action.payload.refreshToken)
        },
        setToken: (
            state: UserState,
            action: PayloadAction<{ token: string; refreshToken: string }>,
        ) => {
            state.refreshToken = action.payload.refreshToken
            state.token = action.payload.token
            localStorage.setItem('token', action.payload.token)
            localStorage.setItem('refreshToken', action.payload.refreshToken)
        },
        setAuthenticated: (
            state: UserState,
            action: PayloadAction<boolean>,
        ) => {
            state.isAuthenticated = action.payload
        },
        unauthenticate: (state: UserState) => {
            state.isAuthenticated = false
            state.user = null
            state.token = ''
            state.refreshToken = ''
            localStorage.clear()
        },
        setEmailVerified: (
            state: UserState,
            action: PayloadAction<boolean>,
        ) => {
            if (state.user) {
                state.user.emailVerified = action.payload
            }
        },
    },
})

export const userActions = userSlice.actions
export default userSlice.reducer
