
#[macro_export]
macro_rules! dict {
    {
        $($key:literal : $value:expr),* $(,)*
    } => {
        $(
            const _: &'static str = $key;
            println!("Key: {} - Value: {}", $key, $value);
        )*
    };
}
