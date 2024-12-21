import { useEffect } from 'react'
import { useState } from 'react'

export default function SharableUser() {
    const [users, setUsers] = useState<{ id: string; email: string }[]>([])

    const fetchUsers = async () => {
        try {
            const response = await fetch('/api/users') // Adjust the API endpoint as necessary
            const data = await response.json()
            setUsers(data)
        } catch (error) {
            console.error('Failed to fetch users:', error)
        }
    }

    const handleDeleteUser = async (userId: string) => {
        try {
            await fetch(`/api/users/${userId}`, { method: 'DELETE' }) // Adjust the API endpoint as necessary
            setUsers(prevUsers => prevUsers.filter(user => user.id !== userId))
        } catch (error) {
            console.error('Failed to delete user:', error)
        }
    }

    useEffect(() => {
        fetchUsers()
    }, [])

    // Render the list of users
    return (
        <div>
            <h2>Share with Users</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>
                        {user.email}
                        <button onClick={() => handleDeleteUser(user.id)}>
                            Delete
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    )
}
