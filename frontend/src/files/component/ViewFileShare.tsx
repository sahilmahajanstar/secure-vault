import { File, FilePermissions } from '../type/file'
import { fileShareLinkApi, filesApi } from '../../config/api/files'
import { useEffect, useState } from 'react'

import Download from './Download'
import { If } from '../../common/components/If'
import View from './View'
import { hasPermission } from '../utils/permission'
import { useAppSelector } from '../../config/redux/hooks'
import { useParams } from 'react-router-dom'

export default function ViewFileShare() {
    const { id } = useParams()
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(true)
    const [permissions, setPermissions] = useState<FilePermissions[]>([])
    const isAuthenticated = useAppSelector(state => state.user.isAuthenticated)
    const user = useAppSelector(state => state.user.user)
    const [error, setError] = useState<string | null>(null)
    const getShareLink = async () => {
        try {
            if (!id) return
            const res = await fileShareLinkApi.getShareLink(id)
            const resFile = await filesApi.downloadFile(res.shareLink.fileId, {
                includeFileShare: true,
                includeFile: false,
                authenticated: isAuthenticated,
            })
            setFile(resFile.file)
            setPermissions(resFile.file.userFileShareInfo?.permissions || [])
            setLoading(false)
        } catch (err) {
            setLoading(false)
            setError((err as Error).message)
        }
    }

    useEffect(() => {
        getShareLink()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    if (!file && !loading) {
        return (
            <div>
                <p>
                    {error ||
                        'File not found or you have no permission to view this file'}
                </p>
            </div>
        )
    }

    return (
        <div
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
            }}>
            <If condition={loading}>
                <p>Loading...</p>
            </If>
            <If condition={!loading && typeof file !== 'undefined'}>
                <div
                    style={{
                        display: 'flex',
                        width: '400px',
                        flexDirection: 'row',
                        alignItems: 'center',
                        justifyContent: 'center',
                        alignSelf: 'center',
                        alignContent: 'center',
                    }}>
                    <If
                        condition={hasPermission(
                            'download',
                            file!,
                            user!,
                            permissions,
                        )}>
                        <Download file={file!} />
                    </If>
                    <If
                        condition={hasPermission(
                            'view',
                            file!,
                            user!,
                            permissions,
                        )}>
                        <View openDefault={true} file={file!} />
                    </If>
                </div>
            </If>
        </div>
    )
}
