import React from "react";
import "../styles/Welcome.css";
import { Link } from "react-router-dom";
function Welcome(){
    return <div className="Welcome">
        <header>
            {/* <div className="menu">
                <ul>
                    <Link to="/login">
                        <li>Login</li>
                    </Link>
                    <Link to="/register">
                        <li>Sign Up</li>
                    </Link>
                    
                </ul>
            </div> */}
                <div className="Title">
                    <div className="content">
                        <p>Welcome to UIC Campus Navigator</p>
                        <p id="subtitle">Your one stop to all campus related inquiries</p>
                        <div className="action">
                            <p>Already a member? Pick up where you left off </p>
                            <Link to="/login">
                                    <button>Login</button>
                            </Link> 
                            
                            <p>Sign Up to get started!</p>
                                <Link to="/register">
                                    <button>Sign Up</button>
                                </Link>
                        </div>
                    </div>    

                    <img src="https://today.uic.edu/wp-content/uploads/2024/10/678a3908_mh_websize.jpg" width="550" height="400" alt="UIC"/>  
                </div>
                <div className="about">
                    <div>
                        <p>About</p>
                    </div>
                    <div>
                        <p>This webapp gives commuter and non-commuter a schedule 
                            that accounts for their class times as well as the train and busses 
                            schedule of the student.
                        </p>
                    </div>
                </div>
                <div className="review">
                    <div className="slides">
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg" alt="UIC" />
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg" alt="UIC"/>
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg"  alt="UIC"/>
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg" alt="UIC"/>
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg" alt="UIC"/>
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg" alt="UIC"/>
                        <img src="https://i.pinimg.com/1200x/53/4b/dd/534bddb03d2e8ab2f6c687f30b13ff2f.jpg" alt="UIC"/>
                    </div>
                </div>
        </header>
        <footer>
            <div className="footer-text">
                <div className="footer-section">
                    <h3>About Us</h3>
                    <p>We built a automatic scheduler for UIC students.</p>
                </div>
                <div className="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <Link to="/login"><li>Login</li>
                        </Link>
                        <Link to="/register"><li>Sign Up</li>
                        </Link>
                        <Link to="/"><li>Welcome</li>
                        </Link>
                    </ul>
                </div>
            </div>
            <div className="footer-section">
                <h3>Follow Us</h3>
                <a href="https://www.instagram.com/thisisuic/?hl=en"><i className="fa-brands fa-uic"></i></a>
                <a href="https://www.instagram.com/uic_cs/?hl=en"><i className="fa-brands fa-uicCS"></i></a>
                <a href="https://www.instagram.com/uicengineering/?hl=en"><i className="fa-brands fa-uicEng"></i></a>
            </div>
            <div className="footer-bottom">
                <p>© 2025 CS 351. All rights reserved</p>
            </div>
        </footer>
    </div>
}

export default Welcome;