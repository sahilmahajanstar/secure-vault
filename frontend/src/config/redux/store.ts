import { persistReducer, persistStore } from 'redux-persist'

import { configureStore } from '@reduxjs/toolkit'
import rootReducer from './reducer'
import storage from 'redux-persist/lib/storage'

const persistConfig = {
    key: 'root',
    storage,
    whitelist: ['user'], // Only persist auth state
}

const persistedReducer = persistReducer(persistConfig, rootReducer)

export const store = configureStore({
    reducer: persistedReducer,
})

export const persistor = persistStore(store)

export type RootState = ReturnType<typeof rootReducer>
export type AppDispatch = typeof store.dispatch

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function dispatch(action: any) {
    return store.dispatch(action)
}
