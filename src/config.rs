use color_eyre::eyre::Result;

#[derive(Debug, Clone)]
pub struct Config {
    pub database_url: String,
    pub jwt_secret: String,
    pub jwt_expires_in: String,
    pub jwt_maxage: i32,
}

impl Config {
    pub fn init() -> Result<Config> {
        let database_url = std::env::var("DATABASE_UR")?;
        let jwt_secret = std::env::var("JWT_SECRET")?;
        let jwt_expires = std::env::var("JWT_EXPIRED_IN")?;
        let jwt_maxage = std::env::var("JWT_MAXAGE")?;
        Config {
            database_url,
            jwt_secret,
            jwt_expires_in,
            jwt_maxage: jwt_maxage.parse::<i32>()?,
        }
    }
}
