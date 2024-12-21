import { PayloadAction, createSlice } from '@reduxjs/toolkit'

import { FilePermissions } from '../type/file'

interface FileState {
    filesData: {
        [key: string]: {
            permissions: FilePermissions[]
            blob: string
        }
    }
}

const initialState: FileState = {
    filesData: {},
}

const fileSlice = createSlice({
    name: 'file',
    initialState,
    reducers: {
        setFiles: (
            state: FileState,
            action: PayloadAction<{
                id: string
                blob: string
                permissions: FilePermissions[]
            }>,
        ) => {
            state.filesData[action.payload.id] = {
                blob: action.payload.blob,
                permissions: action.payload.permissions,
            }
        },
        clearFiles: (state: FileState) => {
            state.filesData = {}
        },
        clearFilesWithId: (state: FileState, action: PayloadAction<string>) => {
            delete state.filesData[action.payload]
        },
    },
})

export const fileActions = fileSlice.actions
export default fileSlice.reducer
