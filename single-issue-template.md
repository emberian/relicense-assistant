The project maintainer explicitly agreed to have this issue opened.

TL;DR the Rust ecosystem is largely Apache-2.0. Being available under that
license is good for interoperation. The MIT license as an add-on can be nice
for GPLv2 projects to use your code.

# Why?

The MIT license requires reproducing countless copies of the same copyright
header with different names in the copyright field, for every MIT library in
use. The Apache license does not have this drawback. However, this is not the
primary motivation for me creating these issues. The Apache license also has
protections from patent trolls and an explicit contribution licensing clause.
However, the Apache license is incompatible with GPLv2. This is why Rust is
dual-licensed as MIT/Apache (the "primary" license being Apache, MIT only for
GPLv2 compat), and doing so would be wise for this project. This also makes
this crate suitable for inclusion and unrestricted sharing in the Rust
standard distribution and other projects using dual MIT/Apache, such as my
personal ulterior motive, [the Robigalia project](https://robigalia.org).

Some ask, "Does this really apply to binary redistributions? Does MIT really
require reproducing the whole thing?" I'm not a lawyer, and I can't give legal
advice, but some Google Android apps include open source attributions using
this interpretation. [Others also agree with
it](https://www.quora.com/Does-the-MIT-license-require-attribution-in-a-binary-only-distribution).

But, again, the copyright notice redistribution is not the primary motivation
for the dual-licensing. Stronger protections to licensees and better
interoperation with the wider Rust ecosystem is.

# How?

To do this, get explicit approval from each contributor of copyrightable
work (as not all contributions qualify for copyright, due to not being a
"creative work", e.g. a typo fix. The advice the FSF uses is "less than
15 lines") and then add the following to your README:

```
## License

Licensed under either of

 * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
 * MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.

### Contribution

Unless you explicitly state otherwise, any contribution intentionally
submitted for inclusion in the work by you, as defined in the Apache-2.0
license, shall be dual licensed as above, without any additional terms
or conditions.
```

and in your license headers, if you have them, use the following boilerplate
(based on that used in Rust):

```
// Copyright 2016 {{project_name}} Developers
//
// Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
// http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
// http://opensource.org/licenses/MIT>, at your option. This file may not be
// copied, modified, or distributed except according to those terms.
```

It's commonly asked whether license headers are required. I'm not comfortable
making an official recommendation either way, but the Apache license
recommends it in their appendix on how to use the license.

Be sure to add the relevant `LICENSE-{MIT,APACHE}` files. You can copy these
from the [Rust](https://github.com/rust-lang/rust) repo for a plain-text
version.

And don't forget to update the `license` metadata in your `Cargo.toml` to:

    license = "MIT OR Apache-2.0"

I'll be going through projects which agree to be relicensed and have approval
by the necessary contributors and doing this changes, so feel free to leave
the heavy lifting to me!

# Contributor checkoff

To agree to relicensing, comment with:

    I license past and future contributions under the dual MIT/Apache-2.0 license, allowing licensees to chose either at their option.

Or, if you're a contributor, you can check the box in this repo next to your
name. My scripts will pick this exact phrase up and check your checkbox, but
I'll come through and manually review this issue later as well.
