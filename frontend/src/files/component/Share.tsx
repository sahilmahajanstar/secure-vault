import '../style/modal.css'
import '../style/share.css'

import { File, FileShare } from '../type/file'
import {
    FileShareLinkRequestBuilder,
    FileShareRequestBuilder,
} from '../../config/api/files/builder'
import { fileShareApi, fileShareLinkApi } from '../../config/api/files'
import { useEffect, useMemo, useRef, useState } from 'react'

import { If } from '../../common/components/If'
import { Modal } from '@mui/material'
import { User } from '../../users/type/user'

const UserList = ({
    users,
    handleRemoveUser,
}: {
    users: User[]
    handleRemoveUser: (user: User) => void
}) => {
    return (
        <div className="user-list">
            {users.map(user => (
                <div key={user.id} className="user-item">
                    {user.email}
                    <span
                        style={{ cursor: 'pointer', marginLeft: '10px' }}
                        onClick={() => handleRemoveUser(user)}>
                        &times;
                    </span>
                </div>
            ))}
        </div>
    )
}

const FileShareList = ({
    fileShares,
    revokeAccess,
}: {
    fileShares: { user: User | null; fileShare: FileShare | null }[]
    revokeAccess: (fileShare: {
        user: User | null
        fileShare: FileShare | null
    }) => void
}) => {
    return (
        <div
            className="user-list"
            style={{
                display: 'flex',
                flexDirection: 'row',
                columnCount: 2,
                justifyContent: 'center',
                alignContent: 'center',
            }}>
            {fileShares.map(fileShare => (
                <div
                    key={fileShare.user?.id}
                    className="user-item"
                    style={{ flex: 1 }}>
                    {fileShare.user?.email}
                    <span
                        style={{
                            cursor: 'pointer',
                            marginLeft: '10px',
                            flex: 1,
                        }}
                        onClick={() =>
                            revokeAccess({
                                user: fileShare.user,
                                fileShare: fileShare.fileShare,
                            })
                        }>
                        &times;
                    </span>
                    <p style={{ alignSelf: 'flex-start' }}>
                        {fileShare.fileShare?.permissions
                            .map(p => p.name)
                            .join(', ')}
                    </p>
                </div>
            ))}
        </div>
    )
}

const ShareFile = ({
    open,
    onClose,
    file,
}: {
    open: boolean
    onClose: () => void
    file: File | null
}) => {
    const [email, setEmail] = useState('')
    const searchUserRef = useRef<NodeJS.Timeout | null>(null)
    const [searchResults, setSearchResults] = useState<User[]>([])
    const [selectedUsers, setSelectedUsers] = useState<User[]>([])
    const createFileShareLink = useMemo(
        () => new FileShareLinkRequestBuilder(),
        [],
    )
    const [showMore, setShowMore] = useState(false)
    const [fileShares, setFileShares] = useState<
        { fileShare: FileShare | null; user: User | null }[]
    >([])
    const [permissions, setPermissions] = useState({
        view: false,
        download: false,
    })
    const [isPublic, setIsPublic] = useState(false)
    const [message, setMessage] = useState('')

    useEffect(() => {
        if (!open) {
            setMessage('')
            setSelectedUsers([])
            setSearchResults([])
            setEmail('')
            setPermissions({
                view: false,
                download: false,
            })
            setIsPublic(false)
        }
    }, [open])
    useEffect(() => {
        if (file) {
            setIsPublic(file.shareType === 'public')
        }
    }, [file])

    const loadFileShareUsers = async () => {
        if (!file?.id) {
            return
        }
        const res = await fileShareApi.getFileShareUsers(file?.id)
        setFileShares(res.fileShareUsers)
    }

    const revokeAccess = async (fileShare: {
        user: User | null
        fileShare: FileShare | null
    }) => {
        if (!fileShare.fileShare?.id) {
            return
        }
        await fileShareApi.revokeAccess(fileShare.fileShare.id)
        setFileShares(
            fileShares.filter(
                fs => fs.fileShare?.id !== fileShare.fileShare?.id,
            ),
        )
    }

    useEffect(() => {
        loadFileShareUsers()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [file])

    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value)
        if (searchUserRef.current) {
            clearTimeout(searchUserRef.current)
        }
        searchUserRef.current = setTimeout(async () => {
            if (e.target.value.length > 0 && file?.id) {
                const res = await fileShareApi.searchUser({
                    fileId: file?.id,
                    email: e.target.value,
                })
                setSearchResults(res.users.filter((u): u is User => u !== null))
            }
            searchUserRef.current = null
        }, 700)
    }

    const handlePermissionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, checked } = e.target
        setPermissions(prev => ({ ...prev, [name]: checked }))
    }

    const handleSelectUser = (user: User) => {
        setSearchResults([])
        for (const u of selectedUsers) {
            if (u.id === user.id) {
                return
            }
        }
        setSelectedUsers([...selectedUsers, user])
    }

    const handleRemoveUser = (user: User) => {
        setSelectedUsers(selectedUsers.filter(u => u.id !== user.id))
    }

    const handleShareFile = async () => {
        if (!file?.id) {
            return
        }
        const perm = Object.entries(permissions)
            .filter(p => p[1])
            .map(p => p[0])
        try {
            const request = new FileShareRequestBuilder()
                .setFileId(file?.id)
                .setUsers(selectedUsers, perm)
                .setShareType(isPublic ? 'public' : 'private')
            const res = await fileShareApi.shareFile(request)
            setIsPublic(res.file.shareType === 'public')
            setSelectedUsers([])
            setMessage('')
            loadFileShareUsers()
            alert('Updated successfully')
        } catch (e) {
            setMessage((e as Error).message)
        }
    }

    const handleCreateLink = async () => {
        if (!file?.id || !createFileShareLink.expires_in_hours) {
            return
        }
        createFileShareLink.setFileId(file?.id)
        const res = await fileShareLinkApi.createLink(createFileShareLink)
        setShowMore(false)
        alert(
            `Link created: ${window.location.origin}/files/share/link/${res.shareLink.id}`,
        )
    }
    if (!open) return null

    return (
        <If condition={open}>
            <Modal key={file?.id} open={open} onClose={onClose}>
                <div
                    style={{
                        justifyContent: 'center',
                        display: 'flex',
                        marginTop: '100px',
                    }}>
                    <span className="close" onClick={onClose}>
                        &times;
                    </span>
                    <div
                        className="modal-content"
                        style={{
                            backgroundColor: '#1a1a1a',
                            maxHeight: '600px',
                            overflowY: 'auto',
                            alignSelf: 'center',
                            flexDirection: 'column',
                        }}>
                        <h5>File Access Info</h5>
                        <button
                            className="fa fa-ellipsis-v"
                            onClick={() => setShowMore(!showMore)}
                            style={{
                                position: 'absolute',
                                right: '20px',
                                top: '20px',
                            }}
                        />
                        <div style={{ position: 'relative' }}>
                            <If condition={showMore}>
                                <div
                                    style={{
                                        position: 'absolute',
                                        right: '-10px',
                                        top: '-20px',
                                        width: '250px',
                                        cursor: 'pointer',
                                        backgroundColor: 'black',
                                        borderRadius: '10px',
                                        zIndex: 100,
                                    }}>
                                    <div
                                        style={{
                                            borderRadius: '5px',
                                            padding: '10px',
                                            backgroundColor: 'black',
                                            color: 'white',
                                            display: 'flex',
                                            flexDirection: 'column',
                                        }}>
                                        <p>Create link</p>
                                        <input
                                            type="number"
                                            placeholder="Enter hours to create Link"
                                            max={24}
                                            style={{
                                                height: '20px',
                                                borderRadius: '5px',
                                                border: '1px solid #333333',
                                                padding: '10px',
                                                marginTop: '10px',
                                            }}
                                            onChange={e => {
                                                if (
                                                    Number(e.target.value) > 24
                                                ) {
                                                    alert(
                                                        'Expires in hours cannot be greater than 24',
                                                    )
                                                    return
                                                }
                                                createFileShareLink.setExpiresInHours(
                                                    Number(e.target.value),
                                                )
                                            }}
                                        />
                                        <div
                                            style={{
                                                display: 'flex',
                                                flexDirection: 'row',
                                                justifyContent: 'space-between',
                                            }}>
                                            <button
                                                style={{
                                                    marginTop: '10px',
                                                    color: 'white',
                                                    padding: '10px 20px',
                                                    borderRadius: '5px',
                                                    alignSelf: 'center',
                                                    zIndex: 1,
                                                }}
                                                onClick={handleCreateLink}>
                                                Create
                                            </button>
                                            <button
                                                style={{
                                                    marginTop: '10px',
                                                    color: 'white',
                                                    padding: '10px 20px',
                                                    borderRadius: '5px',
                                                    alignSelf: 'center',
                                                    zIndex: 1,
                                                }}
                                                onClick={() => {
                                                    setShowMore(false)
                                                }}>
                                                Close
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </If>
                        </div>
                        <label
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                marginTop: '10px',
                                marginBottom: '20px',
                                marginRight: '20px',
                            }}>
                            <input
                                type="checkbox"
                                style={{ width: '20px', height: '20px' }}
                                checked={isPublic}
                                onChange={() => setIsPublic(!isPublic)}
                            />
                            Public Access
                        </label>
                        <h5>Share with users</h5>
                        <div className="form-group">
                            <input
                                type="text"
                                value={email}
                                onChange={handleEmailChange}
                                placeholder="Enter email"
                            />
                            <If condition={email && searchResults.length > 0}>
                                <div className="search-results">
                                    {searchResults.map(user => (
                                        <div
                                            key={user.id}
                                            className="search-result-item">
                                            <p>{user.email}</p>
                                            <button
                                                onClick={() =>
                                                    handleSelectUser(user)
                                                }>
                                                Add
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </If>
                            <UserList
                                users={selectedUsers}
                                handleRemoveUser={handleRemoveUser}
                            />

                            <div
                                style={{
                                    display: 'flex',
                                    flexDirection: 'row',
                                    marginLeft: '10px',
                                    alignItems: 'center',
                                }}>
                                <p style={{ marginRight: '10px' }}>
                                    Permissions:
                                </p>
                                <label>
                                    <input
                                        type="checkbox"
                                        name="view"
                                        checked={permissions.view}
                                        onChange={handlePermissionChange}
                                    />
                                    View
                                </label>
                                <label style={{ marginLeft: '10px' }}>
                                    <input
                                        type="checkbox"
                                        name="download"
                                        checked={permissions.download}
                                        onChange={handlePermissionChange}
                                    />
                                    Download
                                </label>
                            </div>
                        </div>

                        <button
                            style={{
                                backgroundColor: '#4CAF50',
                                color: 'white',
                                padding: '10px 20px',
                                borderRadius: '5px',
                                width: '50%',
                                border: 'none',
                                cursor: 'pointer',
                                alignSelf: 'center',
                            }}
                            onClick={handleShareFile}>
                            Update
                        </button>

                        {message && (
                            <p
                                style={{ alignSelf: 'center' }}
                                className="error-message">
                                {message}
                            </p>
                        )}
                        <If condition={fileShares.length > 0}>
                            <h5
                                style={{
                                    padding: 0,
                                    margin: 0,
                                    marginTop: '40px',
                                }}>
                                Already Share with
                            </h5>
                            <FileShareList
                                fileShares={fileShares}
                                revokeAccess={revokeAccess}
                            />
                        </If>
                    </div>
                </div>
            </Modal>
        </If>
    )
}

export default ShareFile
