class KEYBOARDTELEOP {
  constructor(options) {
    this.that = this
    this.ros = options.ros
    this.topic = options.topic || '/cmd_vel'
    this.max_vel_x = options.max_vel_x || 0.5
    this.max_vel_y = options.max_vel_y || 0.5
    this.max_vel_theta = options.max_vel_theta || (Math.PI / 2)
    this.acc_lim_x = options.acc_lim_x || 0.1
    this.acc_lim_y = options.acc_lim_y || 0.1
    this.acc_lim_theta = options.acc_lim_theta || (Math.PI / 10)
    this.current_x = 0
    this.current_y = 0
    this.current_theta = 0
    this.set_x = options.init_x || this.max_vel_x / 2
    this.set_y = options.init_y || this.max_vel_y / 2
    this.set_theta = options.init_theta || this.max_vel_theta / 2
    this.theta_lock = 0
    this.x_lock = 0
    this.y_lock = 0
    this.cmdVel = new ROSLIB.Topic({
      ros: this.ros,
      name: this.topic,
      messageType: 'geometry_msgs/Twist'
    })
  }
  handleKeyDown(keyEvent) {
    var ispub = false
    switch (keyEvent.key) {
      case 'ArrowUp':
        if (this.x_lock !== -1) {
          this.current_x = this.set_x
          this.x_lock = 1
          ispub = true
        }
        break
      case 'ArrowLeft':
        if (keyEvent.altKey) {
          if (this.y_lock !== -1) {
            this.current_y = this.set_y
            this.y_lock = 1
            ispub = true
          }
        } else {
          if (this.theta_lock !== -1) {
            this.current_theta = this.set_theta
            this.theta_lock = 1
            ispub = true
          }
        }
        break
      case 'ArrowRight':
        if (keyEvent.altKey) {
          if (this.y_lock !== 1) {
            this.current_y = -this.set_y
            this.y_lock = -1
            ispub = true
          }
        } else {
          if (this.theta_lock !== 1) {
            this.current_theta = -this.set_theta
            this.theta_lock = -1
            ispub = true
          }
        }
        break
      case 'ArrowDown':
        if (this.x_lock !== 1) {
          this.current_x = -this.set_x
          this.x_lock = -1
          ispub = true
        }
        break
      default:
        break
    }

    if (ispub) {
      this.pubCmd()
    }
  }
  handleKeyUp(keyEvent) {
    var ispub = false
    switch (keyEvent.key) {
      case 'ArrowUp':
        if (this.x_lock === 1) {
          this.current_x = 0
          this.x_lock = 0
          ispub = true
        }
        break
      case 'ArrowLeft':
        if (keyEvent.altKey) {
          if (this.y_lock === 1) {
            this.current_y = 0
            this.y_lock = 0
            ispub = true
          }
        } else {
          if (this.theta_lock === 1) {
            this.current_theta = 0
            this.theta_lock = 0
            ispub = true
          }
        }
        break
      case 'ArrowRight':
        if (keyEvent.altKey) {
          if (this.y_lock === -1) {
            this.current_y = 0
            this.y_lock = 0
            ispub = true
          }
        } else {
          if (this.theta_lock === -1) {
            this.current_theta = 0
            this.theta_lock = 0
            ispub = true
          }
        }
        break
      case 'ArrowDown':
        if (this.x_lock === -1) {
          this.current_x = 0
          this.x_lock = 0
          ispub = true
        }
        break
      case 'c':
        if (keyEvent.altKey) {
          this.set_y -= this.acc_lim_y
        } else {
          this.set_theta -= this.acc_lim_theta
        }
        this.set_x -= this.acc_lim_x
        this.set_x = this.set_x < 0 ? 0 : this.set_x
        this.set_theta = this.set_theta < 0 ? 0 : this.set_theta
        this.set_y = this.set_y < 0 ? 0 : this.set_y
        break
      case 'v':
        this.set_x -= this.acc_lim_x
        this.set_x = this.set_x < 0 ? 0 : this.set_x
        break
      case 'b':
        if (keyEvent.altKey) {
          this.set_y -= this.acc_lim_y
          this.set_y = this.set_y < 0 ? 0 : this.set_y
        } else {
          this.set_theta -= this.acc_lim_theta
          this.set_theta = this.set_theta < 0 ? 0 : this.set_theta
        }
        break
      case 'e':
        if (keyEvent.altKey) {
          this.set_y += this.acc_lim_y
        } else {
          this.set_theta += this.acc_lim_theta
        }
        this.set_x += this.acc_lim_x
        this.set_x = this.set_x > this.max_vel_x ? this.max_vel_x : this.set_x
        this.set_theta = this.set_theta > this.max_vel_theta ? this.max_vel_theta : this.set_theta
        this.set_y = this.set_y > this.max_vel_y ? this.max_vel_y : this.set_y
        break
      case 'r':
        this.set_x += this.acc_lim_x
        this.set_x = this.set_x > this.max_vel_x ? this.max_vel_x : this.set_x
        break
      case 't':
        if (keyEvent.altKey) {
          this.set_y += this.acc_lim_y
          this.set_y = this.set_y > this.max_vel_y ? this.max_vel_y : this.set_y
        } else {
          this.set_theta += this.acc_lim_theta
          this.set_theta = this.set_theta > this.max_vel_theta ? this.max_vel_theta : this.set_theta
        }
        break
      case 'Alt':
        this.current_y = 0
        break
      default:
        break
    }
    if (ispub) {
      this.pubCmd()
    }
  }
  pubCmd() {
    var twist = new ROSLIB.Message({
      angular: {
        x: 0,
        y: 0,
        z: this.current_theta
      },
      linear: {
        x: this.current_x,
        y: this.current_y,
        z: 0
      }
    })
    this.cmdVel.publish(twist)
  }
}
export default KEYBOARDTELEOP
