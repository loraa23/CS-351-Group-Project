import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import api from "../api"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"
import "../styles/Form.css"

function Form({ route, method }) {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const name = method === "login" ? "Login" : "Register"

    const handleSubmit = async (e) => {
        setLoading(true)
        e.preventDefault()

        try {
            const res = await api.post(route, { username, password })
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access)
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
                navigate("/home")
            } else {
                navigate("/home")
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="App">
            <div className="image-carsole">
                <div className="images">
                        <img src="https://today.uic.edu/wp-content/uploads/2025/08/2025-convocation-drone-h-mh-6x4-1.png" alt="UIC"/>
                        <img src="https://today.uic.edu/wp-content/uploads/2024/10/681A2075_JF2024web.jpg" alt="UIC"/>
                        <img src="https://today.uic.edu/wp-content/uploads/2024/10/678a3200_mh_websie.jpg" alt="UIC"/>
                        <img src="https://today.uic.edu/wp-content/uploads/2025/09/2025-sparkfest-9263-6x4.jpg" alt="UIC"/>
                        <img src="https://today.uic.edu/wp-content/uploads/2024/10/681A1533.campus.jpg" alt="UIC"/>
                        <img src="https://today.uic.edu/wp-content/uploads/2024/10/678a5090_mh_websize.jpg" alt="UIC"/>
                        <img src="https://today.uic.edu/wp-content/uploads/2024/10/678a6682_mh_websize.jpg" alt="UIC"/>
                    </div>
            </div>
            <form onSubmit={handleSubmit} className="form-container">
                <h1>{name}</h1>
                <input
                    className="form-input"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />
                <input
                    className="form-input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <button className="form-button" type="submit" disabled={loading}>
                    {loading ? "Loading..." : name}
                </button>

                {/* Conditional text and link */}
                <div className="form-footer">
                    {method === "login" ? (
                        <p>
                            Don't have an account?{" "}
                            <Link to="/register" className="form-link">Register</Link>
                        </p>
                    ) : (
                        <p>
                            Already have an account?{" "}
                            <Link to="/login" className="form-link">Login</Link>
                        </p>
                    )}
                </div>
            </form>
        </div>
    )
}

export default Form;
