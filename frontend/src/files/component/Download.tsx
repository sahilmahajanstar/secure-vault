import { useAppDispatch, useAppSelector } from '../../config/redux/hooks'

import { File } from '../type/file'
import { MenuItem } from '@mui/material'
import { decryptFile } from '../../utils/webCrypto'
import { fileActions } from '../reducer/fileReducer'
import { filesApi } from '../../config/api/files'
import { hasPermission } from '../utils/permission'
import { useCallback } from 'react'

export default function Download({ file }: { file: File }) {
    const files = useAppSelector(state => state.file.filesData)
    const isAuthenticated = useAppSelector(state => state.user.isAuthenticated)
    const user = useAppSelector(state => state.user.user)
    const dispatch = useAppDispatch()
    const handleDownload = useCallback(async () => {
        let data = files[file.id]
        if (!data) {
            const res = await filesApi.downloadFile(file.id, {
                includeFile: true,
                authenticated: isAuthenticated,
                includeFileShare: true,
            })
            const blob = await decryptFile(res.data)
            const url = window.URL.createObjectURL(blob)
            data = {
                blob: url,
                permissions: res.file?.userFileShareInfo?.permissions || [],
            }
            dispatch(fileActions.setFiles({ id: file.id, ...data }))
        }
        if (hasPermission('download', file, user!, data.permissions)) {
            const a = document.createElement('a')
            a.href = data.blob
            a.download = file.name
            a.click()
        } else {
            alert("You don't have permission to download this file")
        }
    }, [dispatch, file, files, isAuthenticated, user])
    if (
        !user ||
        !hasPermission(
            'download',
            file,
            user,
            file.userFileShareInfo?.permissions ?? [],
        )
    )
        return null
    return (
        <MenuItem style={{ color: 'white' }} onClick={handleDownload}>
            Download
        </MenuItem>
    )
}
