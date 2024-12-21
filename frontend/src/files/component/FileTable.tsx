import '../style/listFile.css'

import { DataGrid, GridColDef, useGridApiRef } from '@mui/x-data-grid'
import React, { useState } from 'react'

import Download from './Download'
import { File } from '../type/file'
import { If } from '../../common/components/If'
import Menu from '@mui/material/Menu'
import { MenuItem } from '@mui/material'
import Paper from '@mui/material/Paper'
import ShareFile from './Share'
import View from './View'
import { filesApi } from '../../config/api/files'
import { useAppSelector } from '../../config/redux/hooks'

export function Options({
    file,
    handleDelete,
    handleShare,
}: {
    file: File
    handleDelete: (fileId: string) => void
    handleShare: (file: File) => void
}) {
    const ITEM_HEIGHT = 48
    const user = useAppSelector(state => state.user.user)

    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null)
    const open = Boolean(anchorEl)
    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget)
    }
    const handleClose = () => {
        setAnchorEl(null)
    }

    return (
        <div>
            <button onClick={handleClick}> Actions</button>
            <Menu
                id="long-menu"
                MenuListProps={{
                    'aria-labelledby': 'long-button',
                }}
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                slotProps={{
                    paper: {
                        style: {
                            maxHeight: ITEM_HEIGHT * 4.5,
                            width: '20ch',
                            backgroundColor: '#343434',
                        },
                    },
                }}>
                <View file={file} openDefault={false} />
                <Download file={file} />
                {/* move to attribute base filter create common object with {file: {create: performcheck, update: performcheck, delete: performcheck}} */}
                <If
                    condition={
                        file.userId === user?.id || user?.role === 'admin'
                    }>
                    <MenuItem
                        style={{ color: 'white' }}
                        onClick={() => handleDelete(file.id)}>
                        Delete
                    </MenuItem>
                    <MenuItem
                        style={{ color: 'white' }}
                        onClick={() => handleShare(file)}>
                        Share
                    </MenuItem>
                </If>
            </Menu>
        </div>
    )
}

export const FileTable = ({
    files,
    reloadList,
    columns: anotherColumns,
    rowCount,
}: {
    files: File[]
    reloadList: (offset: number, limit: number) => void
    columns?: GridColDef[]
    rowCount: number
}) => {
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [selectedFile, setSelectedFile] = React.useState<File | null>(null)
    const apiRef = useGridApiRef()
    const [page, setPage] = React.useState<number>(0)
    const handleDelete = async (fileId: string) => {
        try {
            const res = await filesApi.deleteFile(fileId)
            if (res.file && (rowCount - 1) % 10 > 0) {
                reloadList(page * 10, 10)
            } else {
                apiRef.current.setPage(Math.max(0, page - 1))
                reloadList(Math.max(0, page - 1) * 10, 10)
            }
        } catch (err) {
            console.log(err)
            alert('Failed to delete file')
        }
    }

    const handleShare = (file: File) => {
        setSelectedFile(file)
        setIsModalOpen(true)
    }

    const onClose = () => {
        setIsModalOpen(false)
        setSelectedFile(null)
    }

    const columns: GridColDef[] = [
        {
            field: 'name',
            headerName: 'Name',
            headerClassName: 'header-table',
            flex: 1,
            filterable: false,
            sortable: false,
        },
        {
            field: 'type',
            headerName: 'type',
            headerClassName: 'header-table',
            flex: 1,
            filterable: false,
            sortable: false,
            valueGetter: (_, row) => row.fileMetadata?.type,
        },
        {
            field: 'createdAt',
            headerName: 'created',
            headerClassName: 'header-table',
            flex: 1,
            filterable: false,
            sortable: false,
        },
        {
            field: 'Action',
            headerName: 'Action',
            description: 'This column has a value getter and is not sortable.',
            sortable: false,
            flex: 1,
            filterable: false,
            headerClassName: 'header-table',
            renderCell: params => (
                <Options
                    file={params.row}
                    handleDelete={handleDelete}
                    handleShare={handleShare}
                />
            ),
        },
        ...(anotherColumns ?? []),
    ]

    return (
        <Paper
            sx={{
                height: '90vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                alignSelf: 'center',
                alignContent: 'center',
                backgroundColor: '#242424',
                color: 'white',
                textColor: 'white',
            }}>
            <ShareFile
                open={isModalOpen}
                onClose={onClose}
                file={selectedFile}
            />
            <DataGrid
                apiRef={apiRef}
                style={{ color: 'white' }}
                rows={files}
                columns={columns}
                rowCount={rowCount}
                initialState={{
                    pagination: { paginationModel: { page: 0, pageSize: 10 } },
                }}
                paginationMode="server"
                onPaginationModelChange={model => {
                    setPage(model.page)
                    reloadList(model.page * model.pageSize, model.pageSize)
                }}
                pageSizeOptions={[10]}
                checkboxSelection={false}
                sx={{ border: 0 }}
            />
        </Paper>
    )
}
